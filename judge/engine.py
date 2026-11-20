import os
import shutil
import subprocess
import time
import uuid
from typing import Dict, List, Any

from config import (
    TEMP_EXEC_DIR,
    DEFAULT_TIMEOUT_SECONDS,
    TIMEOUT_BY_LANGUAGE,
    MAX_OUTPUT_LENGTH,
    PYTHON_EXECUTABLE,
    C_COMPILER,
    C_FLAGS
)
from judge.security import check_code_safety


def normalize_output(text: str) -> str:
    """
    Chuan hoa dau ra de so sanh:
    - Bo ky tu \r (xu ly CRLF cua Windows vs LF cua Linux).
    - Cat bo khoang trang thua o cuoi moi dong (trailing spaces).
    - Cat bo cac dong trong thua o dau va cuoi van ban.
    """
    if text is None:
        return ""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").strip().split("\n")
    return "\n".join(line.rstrip() for line in lines)


def truncate_text(text: str, max_len: int = 1500) -> str:
    """Cat bot noi dung neu qua dai de tranh lam nang payload giao dien"""
    if not text:
        return ""
    if len(text) > max_len:
        return text[:max_len] + f"\n... [Đã cắt bớt {len(text) - max_len} ký tự]"
    return text


def get_timeout_for_language(language: str) -> float:
    """Lay gioi han thoi gian rieng biet cho tung ngon ngu lap trinh (C: 1.0s, Python: 2.0s)"""
    lang = language.lower().strip()
    return TIMEOUT_BY_LANGUAGE.get(lang, DEFAULT_TIMEOUT_SECONDS)


def run_code_once(command: List[str], input_data: str, timeout: float = DEFAULT_TIMEOUT_SECONDS, cwd: str = None) -> Dict[str, Any]:
    """
    Thuc thi chuong trinh voi mot bo input_data cu the va do thoi gian.
    Chi tinh thoi gian chay cua file thuc thi, khong tinh thoi gian bien dich.
    """
    start_time = time.perf_counter()
    try:
        process = subprocess.run(
            command,
            input=input_data,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd
        )
        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
        
        stdout = process.stdout if process.stdout else ""
        stderr = process.stderr if process.stderr else ""
        
        if len(stdout) > MAX_OUTPUT_LENGTH:
            stdout = stdout[:MAX_OUTPUT_LENGTH] + "\n[Cảnh báo: Output vượt quá giới hạn hiển thị]"

        return {
            "stdout": stdout,
            "stderr": stderr,
            "returncode": process.returncode,
            "duration_ms": duration_ms,
            "is_tle": False
        }
    except subprocess.TimeoutExpired:
        duration_ms = round(timeout * 1000, 2)
        return {
            "stdout": "",
            "stderr": f"Time Limit Exceeded (Quá giới hạn thời gian {timeout}s)",
            "returncode": -1,
            "duration_ms": duration_ms,
            "is_tle": True
        }
    except Exception as e:
        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
        return {
            "stdout": "",
            "stderr": f"Lỗi hệ thống khi thực thi: {str(e)}",
            "returncode": -1,
            "duration_ms": duration_ms,
            "is_tle": False
        }


def run_custom_test(code: str, language: str, custom_input: str) -> Dict[str, Any]:
    """
    Chay thu ma nguon voi input tuy chon cua nguoi dung (Nut 'Run Code').
    Ap dung dung timeout rieng theo ngon ngu (C: 1.0s, Python: 2.0s).
    """
    # 1. Kiem tra bao mat
    is_safe, sec_msg = check_code_safety(code, language)
    if not is_safe:
        return {
            "success": False,
            "verdict": "SECURITY_VIOLATION",
            "message": sec_msg,
            "stdout": "",
            "stderr": sec_msg,
            "duration_ms": 0
        }

    # 2. Tao thu muc chay tam thoi
    run_id = f"run_{uuid.uuid4().hex}"
    work_dir = os.path.join(TEMP_EXEC_DIR, run_id)
    os.makedirs(work_dir, exist_ok=True)

    lang = language.lower().strip()
    timeout_sec = get_timeout_for_language(lang)

    try:
        if lang in ("c", "gcc"):
            c_file = os.path.join(work_dir, "code.c")
            exe_file = os.path.join(work_dir, "code.exe")
            with open(c_file, "w", encoding="utf-8") as f:
                f.write(code)

            # Biên dịch bằng GCC (thời gian này tách biệt, không tính vào thời gian thực thi)
            compile_cmd = [C_COMPILER] + C_FLAGS + [c_file, "-o", exe_file]
            comp_res = subprocess.run(compile_cmd, capture_output=True, text=True, cwd=work_dir)
            if comp_res.returncode != 0:
                return {
                    "success": False,
                    "verdict": "CE",
                    "message": "Lỗi biên dịch (Compilation Error)",
                    "stdout": "",
                    "stderr": comp_res.stderr,
                    "duration_ms": 0,
                    "timeout_sec": timeout_sec
                }
            run_cmd = [exe_file]

        elif lang in ("python", "python3", "py"):
            py_file = os.path.join(work_dir, "code.py")
            with open(py_file, "w", encoding="utf-8") as f:
                f.write(code)
            run_cmd = [PYTHON_EXECUTABLE, "-u", py_file]

        else:
            return {
                "success": False,
                "verdict": "UNSUPPORTED_LANGUAGE",
                "message": f"Ngôn ngữ '{language}' chưa được hỗ trợ",
                "stdout": "",
                "stderr": "",
                "duration_ms": 0,
                "timeout_sec": timeout_sec
            }

        # 3. Chạy file thực thi với input người dùng và đo thời gian thực tế
        exec_res = run_code_once(run_cmd, custom_input, timeout=timeout_sec, cwd=work_dir)

        if exec_res["is_tle"]:
            verdict = "TLE"
            msg = f"Time Limit Exceeded: Mã nguồn chạy quá giới hạn thời gian {timeout_sec}s cho phép của {lang.upper()}."
        elif exec_res["returncode"] != 0:
            verdict = "RTE"
            msg = f"Runtime Error (Mã thoát {exec_res['returncode']})"
        else:
            verdict = "SUCCESS"
            msg = "Thực thi thành công."

        return {
            "success": (verdict == "SUCCESS"),
            "verdict": verdict,
            "message": msg,
            "stdout": truncate_text(exec_res["stdout"], 3000),
            "stderr": truncate_text(exec_res["stderr"], 3000),
            "duration_ms": exec_res["duration_ms"],
            "timeout_sec": timeout_sec
        }

    finally:
        shutil.rmtree(work_dir, ignore_errors=True)


def judge_submission(
    code: str,
    language: str,
    test_cases: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    He thong cham diem (Judge Engine) tu dong:
    - Áp dụng thời gian giới hạn nghiêm ngặt riêng theo ngôn ngữ: C = 1.0s, Python = 2.0s.
    - Thời gian C chỉ đo thời gian chạy của file thực thi solution.exe, KHÔNG tính thời gian biên dịch gcc.
    - Khi một test case bị TLE, test case đó nhận 0 điểm, nhưng hệ thống VẪN TIẾP TỤC CHẠY các test cases còn lại.
    - Hiển thị chi tiết từng test case: AC, WA, TLE (kèm thời gian thực tế / giới hạn cho phép), RTE.
    """
    lang = language.lower().strip()
    timeout_sec = get_timeout_for_language(lang)

    # 1. Kiem tra bao mat AST / regex
    is_safe, sec_msg = check_code_safety(code, language)
    if not is_safe:
        return {
            "status": "SECURITY_VIOLATION",
            "score": 0,
            "passed_count": 0,
            "total_count": len(test_cases),
            "max_time_ms": 0,
            "timeout_sec": timeout_sec,
            "message": sec_msg,
            "test_results": []
        }

    # 2. Tao thu muc thuc thi doc lap
    run_id = f"sub_{uuid.uuid4().hex}"
    work_dir = os.path.join(TEMP_EXEC_DIR, run_id)
    os.makedirs(work_dir, exist_ok=True)

    try:
        if lang in ("c", "gcc"):
            c_file = os.path.join(work_dir, "solution.c")
            exe_file = os.path.join(work_dir, "solution.exe")
            with open(c_file, "w", encoding="utf-8") as f:
                f.write(code)

            # Biên dịch bằng GCC riêng biệt (không tính vào thời gian của test case)
            compile_cmd = [C_COMPILER] + C_FLAGS + [c_file, "-o", exe_file]
            comp_res = subprocess.run(compile_cmd, capture_output=True, text=True, cwd=work_dir)
            if comp_res.returncode != 0:
                # Lỗi biên dịch (Compilation Error)
                return {
                    "status": "CE",
                    "score": 0,
                    "passed_count": 0,
                    "total_count": len(test_cases),
                    "max_time_ms": 0,
                    "timeout_sec": timeout_sec,
                    "message": "Lỗi biên dịch (Compilation Error)",
                    "compiler_output": comp_res.stderr,
                    "test_results": []
                }
            run_cmd = [exe_file]

        elif lang in ("python", "python3", "py"):
            py_file = os.path.join(work_dir, "solution.py")
            with open(py_file, "w", encoding="utf-8") as f:
                f.write(code)
            run_cmd = [PYTHON_EXECUTABLE, "-u", py_file]

        else:
            return {
                "status": "ERROR",
                "score": 0,
                "passed_count": 0,
                "total_count": len(test_cases),
                "max_time_ms": 0,
                "timeout_sec": timeout_sec,
                "message": f"Ngôn ngữ '{language}' không được hỗ trợ",
                "test_results": []
            }

        # 3. Chay qua toan bo danh sach test cases
        test_results = []
        passed_count = 0
        max_time_ms = 0.0
        first_failure_verdict = None
        has_tle = False

        for idx, tc in enumerate(test_cases, start=1):
            tc_input = tc.get("input_data", "")
            tc_expected = tc.get("expected_output", "")
            tc_desc = tc.get("description", f"Test case #{idx}")
            is_sample = tc.get("is_sample", False)

            # Thực thi và đo thời gian độc lập của từng test case
            exec_res = run_code_once(run_cmd, tc_input, timeout=timeout_sec, cwd=work_dir)
            exec_time = exec_res["duration_ms"]
            max_time_ms = max(max_time_ms, exec_time)

            user_out = exec_res["stdout"]
            user_err = exec_res["stderr"]

            if exec_res["is_tle"]:
                tc_verdict = "TLE"
                has_tle = True
                message = f"Vượt quá thời gian giới hạn ({timeout_sec}s). Thời gian chạy: {exec_time} ms / Giới hạn: {int(timeout_sec * 1000)} ms"
            elif exec_res["returncode"] != 0:
                tc_verdict = "RTE"
                message = user_err if user_err else f"Runtime Error (Mã thoát {exec_res['returncode']})"
            else:
                norm_user = normalize_output(user_out)
                norm_expected = normalize_output(tc_expected)
                if norm_user == norm_expected:
                    tc_verdict = "AC"
                    message = "Chính xác (Accepted)"
                    passed_count += 1
                else:
                    tc_verdict = "WA"
                    message = "Kết quả sai (Wrong Answer)"

            if tc_verdict != "AC" and first_failure_verdict is None:
                first_failure_verdict = tc_verdict

            test_results.append({
                "test_index": idx,
                "description": tc_desc,
                "is_sample": is_sample,
                "verdict": tc_verdict,
                "execution_time_ms": exec_time,
                "timeout_ms": int(timeout_sec * 1000),
                "message": message,
                "input_preview": truncate_text(tc_input, 200),
                "expected_preview": truncate_text(tc_expected, 200),
                "actual_preview": truncate_text(user_out, 200),
                "error_detail": truncate_text(user_err, 300)
            })

        # 4. Tinh toan diem so & trang thai tong quan
        total_tests = len(test_cases)
        score = round((passed_count / total_tests) * 100) if total_tests > 0 else 0

        if passed_count == total_tests:
            final_status = "AC"
            final_message = f"Chúc mừng! Bạn đã vượt qua tất cả {total_tests}/{total_tests} test cases."
        else:
            # Nếu có test bị TLE thì ưu tiên báo TLE để người dùng biết code bị chậm
            if has_tle:
                final_status = "TLE"
            else:
                final_status = first_failure_verdict if first_failure_verdict else "WA"
            final_message = f"Vượt qua {passed_count}/{total_tests} test cases ({score} điểm). Giới hạn thời gian {lang.upper()}: {timeout_sec}s."

        return {
            "status": final_status,
            "score": score,
            "passed_count": passed_count,
            "total_count": total_tests,
            "max_time_ms": max_time_ms,
            "timeout_sec": timeout_sec,
            "message": final_message,
            "test_results": test_results
        }

    finally:
        shutil.rmtree(work_dir, ignore_errors=True)
