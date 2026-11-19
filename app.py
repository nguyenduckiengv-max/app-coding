import json
from flask import Flask, render_template, request, jsonify, abort
from config import HOST, PORT, DEBUG
from models.database import (
    init_db,
    get_all_problems,
    get_problem,
    get_test_cases,
    record_submission,
    get_submissions_for_problem,
    get_overall_stats,
    seed_problems_from_json,
    get_db_connection,
    get_solution
)
from judge.engine import run_custom_test, judge_submission

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

# Khoi tao database luc khoi dong ung dung
init_db()


@app.route("/")
def index():
    """Trang chu: Danh sach bai tap va bang thong ke tong quan"""
    problems = get_all_problems()
    stats = get_overall_stats()
    
    # Lay danh sach cac chuong/phan de lam bo loc
    chapters = sorted(list(set(p["chapter"] for p in problems)))
    
    return render_template(
        "index.html",
        problems=problems,
        stats=stats,
        chapters=chapters
    )


@app.route("/problem/<problem_id>")
def problem_detail(problem_id):
    """Trang chi tiet bai tap voi giao dien 2 cot (LeetCode / HackerRank style)"""
    problem = get_problem(problem_id)
    if not problem:
        abort(404)
    
    submissions = get_submissions_for_problem(problem_id)
    return render_template(
        "problem.html",
        problem=problem,
        submissions=submissions
    )


@app.route("/guide")
def guide():
    """Trang huong dan su dung, them bai tap moi va kien truc he thong"""
    return render_template("guide.html")


# ==================== REST APIs ====================

@app.route("/api/run", methods=["POST"])
def api_run_code():
    """
    API Chay thu code voi Custom Test Input hoac Test Mau.
    Payload: { problem_id, language, code, custom_input }
    """
    data = request.get_json() or {}
    code = data.get("code", "")
    language = data.get("language", "python3")
    custom_input = data.get("custom_input", "")

    if not code.strip():
        return jsonify({
            "success": False,
            "verdict": "EMPTY_CODE",
            "message": "Vui lòng nhập mã nguồn trước khi chạy thử.",
            "stdout": "",
            "stderr": "",
            "duration_ms": 0
        }), 400

    result = run_custom_test(code, language, custom_input)
    return jsonify(result)


@app.route("/api/submit", methods=["POST"])
def api_submit_code():
    """
    API Cham diem ma nguon voi toan bo bo test cases (>= 5 test).
    Payload: { problem_id, language, code }
    """
    data = request.get_json() or {}
    problem_id = data.get("problem_id", "")
    language = data.get("language", "python3")
    code = data.get("code", "")

    if not problem_id:
        return jsonify({"error": "Thiếu mã bài tập (problem_id)"}), 400

    if not code.strip():
        return jsonify({
            "status": "EMPTY_CODE",
            "score": 0,
            "passed_count": 0,
            "total_count": 0,
            "max_time_ms": 0,
            "message": "Vui lòng nhập mã nguồn trước khi nộp bài.",
            "test_results": []
        }), 400

    problem = get_problem(problem_id)
    if not problem:
        return jsonify({"error": f"Không tìm thấy bài tập '{problem_id}'"}), 404

    # Lay toan bo bo test cases cua bai
    test_cases = get_test_cases(problem_id)
    if not test_cases:
        return jsonify({"error": f"Bài tập '{problem_id}' chưa được cấu hình test case."}), 500

    # Cham diem qua Judge Engine
    judge_result = judge_submission(code, language, test_cases)

    # Ghi ket qua submit vao database de theo doi lich su
    submission_id = record_submission(problem_id, language, code, judge_result)
    judge_result["submission_id"] = submission_id

    return jsonify(judge_result)


@app.route("/api/submissions/<problem_id>", methods=["GET"])
def api_get_submissions(problem_id):
    """Lay lich su cac lan nop bai cho mot bai tap"""
    submissions = get_submissions_for_problem(problem_id)
    return jsonify({"submissions": submissions})


@app.route("/api/submission/<int:sub_id>", methods=["GET"])
def api_get_submission_detail(sub_id):
    """Lay chi tiet ma nguon va ket qua tung test cua mot lan nop cu the"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM submissions WHERE id = ?", (sub_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Không tìm thấy lần nộp bài này"}), 404

    sub_dict = dict(row)
    try:
        sub_dict["details"] = json.loads(sub_dict["details_json"])
    except:
        sub_dict["details"] = []
    return jsonify(sub_dict)


@app.route("/api/solution/<problem_id>", methods=["GET"])
def api_get_problem_solution(problem_id):
    """Lay loi giai chi tiet (Editorial) va ma nguon mau cho bai tap"""
    sol = get_solution(problem_id)
    if not sol:
        return jsonify({"error": "Không tìm thấy lời giải cho bài tập này"}), 404
    return jsonify({
        "success": True,
        "problem_id": problem_id,
        "title": sol["title"],
        "editorial": sol["editorial"] or "Hiện chưa có bài viết phân tích chi tiết cho bài tập này.",
        "solution_python": sol["solution_python"] or "# Lời giải Python đang được cập nhật",
        "solution_c": sol["solution_c"] or "// Lời giải C đang được cập nhật"
    })


@app.route("/api/admin/reload-problems", methods=["POST"])
def api_reload_problems():
    """Nap lai du lieu bai tap tu data/problems.json vao database"""
    try:
        seed_problems_from_json()
        return jsonify({"success": True, "message": "Đã đồng bộ lại toàn bộ bài tập và test cases từ JSON thành công!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    print(f"🚀 Khởi động Dragon Judge Platform tại http://localhost:{PORT}")
    app.run(host=HOST, port=PORT, debug=DEBUG)
