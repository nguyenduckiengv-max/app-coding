import json
import os
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional
from config import DB_PATH, PROBLEMS_JSON_PATH


def get_db_connection() -> sqlite3.Connection:
    """Tao ket noi toi co so du lieu SQLite voi row_factory"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Khoi tao cac bang can thiet trong database"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Bang danh sach bai tap
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS problems (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            chapter TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            time_limit REAL DEFAULT 1.5,
            memory_limit INTEGER DEFAULT 256,
            description TEXT NOT NULL,
            input_format TEXT NOT NULL,
            output_format TEXT NOT NULL,
            constraints TEXT NOT NULL,
            sample_input TEXT NOT NULL,
            sample_output TEXT NOT NULL,
            hints TEXT DEFAULT '',
            python_starter TEXT NOT NULL,
            c_starter TEXT NOT NULL,
            solution_python TEXT DEFAULT '',
            solution_c TEXT DEFAULT '',
            editorial TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Kiem tra va them cot moi neu database da ton tai tu truoc
    cursor.execute("PRAGMA table_info(problems)")
    existing_cols = [row["name"] for row in cursor.fetchall()]
    for col in ["solution_python", "solution_c", "editorial"]:
        if col not in existing_cols:
            cursor.execute(f"ALTER TABLE problems ADD COLUMN {col} TEXT DEFAULT ''")

    # Bang bo test cases (toi thieu 5 test cases moi bai)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problem_id TEXT NOT NULL,
            test_index INTEGER NOT NULL,
            input_data TEXT NOT NULL,
            expected_output TEXT NOT NULL,
            is_sample BOOLEAN DEFAULT 0,
            description TEXT DEFAULT '',
            FOREIGN KEY (problem_id) REFERENCES problems(id) ON DELETE CASCADE
        )
    """)

    # Bang lich su nop bai
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problem_id TEXT NOT NULL,
            language TEXT NOT NULL,
            code TEXT NOT NULL,
            status TEXT NOT NULL,
            score INTEGER DEFAULT 0,
            passed_count INTEGER DEFAULT 0,
            total_count INTEGER DEFAULT 0,
            max_time_ms REAL DEFAULT 0,
            details_json TEXT DEFAULT '{}',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (problem_id) REFERENCES problems(id)
        )
    """)

    conn.commit()
    conn.close()

    # Seed du lieu tu problems.json
    seed_problems_from_json()


def seed_problems_from_json(json_path: str = PROBLEMS_JSON_PATH):
    """Doc file JSON chua danh sach bai tap va bo test cases de nap vao Database"""
    if not os.path.exists(json_path):
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    conn = get_db_connection()
    cursor = conn.cursor()

    for item in data.get("problems", []):
        prob_id = item["id"]

        # Insert hoac update bai tap
        cursor.execute("""
            INSERT INTO problems (
                id, title, chapter, difficulty, time_limit, memory_limit,
                description, input_format, output_format, constraints,
                sample_input, sample_output, hints, python_starter, c_starter,
                solution_python, solution_c, editorial
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                title=excluded.title,
                chapter=excluded.chapter,
                difficulty=excluded.difficulty,
                time_limit=excluded.time_limit,
                memory_limit=excluded.memory_limit,
                description=excluded.description,
                input_format=excluded.input_format,
                output_format=excluded.output_format,
                constraints=excluded.constraints,
                sample_input=excluded.sample_input,
                sample_output=excluded.sample_output,
                hints=excluded.hints,
                python_starter=excluded.python_starter,
                c_starter=excluded.c_starter,
                solution_python=excluded.solution_python,
                solution_c=excluded.solution_c,
                editorial=excluded.editorial
        """, (
            prob_id, item["title"], item["chapter"], item.get("difficulty", "Dễ"),
            item.get("time_limit", 1.5), item.get("memory_limit", 256),
            item["description"], item["input_format"], item["output_format"],
            item["constraints"], item["sample_input"], item["sample_output"],
            item.get("hints", ""),
            item.get("python_starter", "# Viết code Python 3 tại đây\n"),
            item.get("c_starter", "// Viết code C tại đây\n#include <stdio.h>\n\nint main() {\n    return 0;\n}\n"),
            item.get("solution_python", ""),
            item.get("solution_c", ""),
            item.get("editorial", "")
        ))

        # Xoa cac test cases cu cua bai nay de nap lai dung chuan
        cursor.execute("DELETE FROM test_cases WHERE problem_id = ?", (prob_id,))

        # Nap bo test cases (bao gom >= 5 test: co ban, bien, stress test)
        for idx, tc in enumerate(item.get("test_cases", []), start=1):
            cursor.execute("""
                INSERT INTO test_cases (
                    problem_id, test_index, input_data, expected_output, is_sample, description
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                prob_id,
                tc.get("test_index", idx),
                tc["input_data"],
                tc["expected_output"],
                1 if tc.get("is_sample", False) else 0,
                tc.get("description", f"Test case #{idx}")
            ))

    conn.commit()
    conn.close()


def get_all_problems() -> List[Dict[str, Any]]:
    """Lay danh sach tat ca cac bai tap kem thong ke trang thai da giai hay chua"""
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            p.*,
            (SELECT COUNT(*) FROM test_cases tc WHERE tc.problem_id = p.id) as test_case_count,
            (SELECT COUNT(*) FROM submissions s WHERE s.problem_id = p.id) as total_submissions,
            (SELECT COUNT(*) FROM submissions s WHERE s.problem_id = p.id AND s.status = 'AC') as accepted_submissions,
            (SELECT MAX(score) FROM submissions s WHERE s.problem_id = p.id) as best_score,
            CASE 
                WHEN EXISTS(SELECT 1 FROM submissions s WHERE s.problem_id = p.id AND s.status = 'AC') THEN 'SOLVED'
                WHEN EXISTS(SELECT 1 FROM submissions s WHERE s.problem_id = p.id) THEN 'ATTEMPTED'
                ELSE 'TODO'
            END as user_status
        FROM problems p
        ORDER BY p.id ASC
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    problems = [dict(row) for row in rows]
    conn.close()
    return problems


def get_problem(problem_id: str) -> Optional[Dict[str, Any]]:
    """Lay chi tiet mot bai tap theo id"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM problems WHERE id = ?", (problem_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None
    problem = dict(row)

    # Lay danh sach test cases mau de hien thi tren giao dien
    cursor.execute("""
        SELECT test_index, input_data, expected_output, description
        FROM test_cases
        WHERE problem_id = ? AND is_sample = 1
        ORDER BY test_index ASC
    """, (problem_id,))
    sample_tests = [dict(r) for r in cursor.fetchall()]
    problem["sample_tests"] = sample_tests

    # Kiem tra xem nguoi dung da submit hoac solve chua
    cursor.execute("SELECT COUNT(*) FROM submissions WHERE problem_id = ?", (problem_id,))
    submission_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM submissions WHERE problem_id = ? AND status = 'AC'", (problem_id,))
    solved_count = cursor.fetchone()[0]

    problem["has_submitted"] = submission_count > 0
    problem["has_solved"] = solved_count > 0

    conn.close()
    return problem


def get_test_cases(problem_id: str) -> List[Dict[str, Any]]:
    """Lay toan bo test cases cua mot bai tap de he thong cham diem (Judge Engine) thuc thi"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT test_index, input_data, expected_output, is_sample, description
        FROM test_cases
        WHERE problem_id = ?
        ORDER BY test_index ASC
    """, (problem_id,))
    rows = cursor.fetchall()
    test_cases = [dict(r) for r in rows]
    conn.close()
    return test_cases


def record_submission(
    problem_id: str,
    language: str,
    code: str,
    judge_result: Dict[str, Any]
) -> int:
    """Luu ket qua submit vao database"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO submissions (
            problem_id, language, code, status, score,
            passed_count, total_count, max_time_ms, details_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        problem_id,
        language,
        code,
        judge_result.get("status", "ERROR"),
        judge_result.get("score", 0),
        judge_result.get("passed_count", 0),
        judge_result.get("total_count", 0),
        judge_result.get("max_time_ms", 0),
        json.dumps(judge_result.get("test_results", []), ensure_ascii=False)
    ))

    sub_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return sub_id


def get_submissions_for_problem(problem_id: str, limit: int = 15) -> List[Dict[str, Any]]:
    """Lay lich su cac lan nop bai gan nhat cho bai tap nay"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, problem_id, language, status, score, passed_count, total_count, max_time_ms, created_at
        FROM submissions
        WHERE problem_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (problem_id, limit))
    rows = cursor.fetchall()
    submissions = [dict(r) for r in rows]
    conn.close()
    return submissions


def get_solution(problem_id: str) -> Optional[Dict[str, Any]]:
    """Lay loi giai chi tiet va code mau cua bai tap"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, editorial, solution_python, solution_c
        FROM problems WHERE id = ?
    """, (problem_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_overall_stats() -> Dict[str, Any]:
    """Lay thong ke tong the he thong"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM problems")
    total_problems = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(DISTINCT problem_id) 
        FROM submissions 
        WHERE status = 'AC'
    """)
    solved_problems = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM submissions")
    total_submissions = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM submissions WHERE status = 'AC'")
    ac_submissions = cursor.fetchone()[0]

    conn.close()
    return {
        "total_problems": total_problems,
        "solved_problems": solved_problems,
        "total_submissions": total_submissions,
        "ac_rate": round((ac_submissions / total_submissions * 100), 1) if total_submissions > 0 else 0
    }
