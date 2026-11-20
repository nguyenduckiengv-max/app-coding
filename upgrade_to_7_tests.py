# Script to upgrade problems 50 to 100 to have 7 test cases with large / stress test inputs
import json
import subprocess
import sys
import os

from config import PYTHON_EXECUTABLE

with open('data/problems.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    problems = data['problems']

def run_py_solution(code, input_str):
    """Run python solution directly and return stdout"""
    proc = subprocess.run(
        [PYTHON_EXECUTABLE, "-c", code],
        input=input_str,
        capture_output=True,
        text=True,
        timeout=10
    )
    if proc.returncode != 0:
        raise RuntimeError(f"Solution error: {proc.stderr}")
    return proc.stdout

# Define specialized test 6 and test 7 inputs for problems 50 to 100
special_inputs = {
    "DRAGON-50": [
        ("987654 321 876543 999\n", "Test số lớn hỗn hợp"),
        ("1000 -1000 1000 -1000\n", "Test biên âm dương")
    ],
    "DRAGON-51": [
        ("999999999 333333333\n", "Rút gọn phân số lớn"),
        ("1000000 800000\n", "Phân số triệu")
    ],
    "DRAGON-52": [
        ("9999.85 8888.75\n", "Kích thước chữ nhật lớn"),
        ("0.05 0.12\n", "Kích thước chữ nhật cực nhỏ")
    ],
    "DRAGON-53": [
        ("9999.99\n", "Cạnh hình vuông lớn sát 10000"),
        ("1234.56\n", "Cạnh lẻ thập phân")
    ],
    "DRAGON-54": [
        ("999999937\n", "Số nguyên tố lớn (chỉ 1 thừa số)"),
        ("987654321\n", "Phân tích số lớn nhiều thừa số")
    ],
    "DRAGON-55": [
        ("999999998\n", "Số chẵn cực lớn"),
        ("999999999\n", "Số lẻ cực lớn sát 10^9")
    ],
    "DRAGON-56": [
        ("999999999\n", "Tổng 3 số chia hết cho 3 (YES)"),
        ("1000000000\n", "Số lớn không chia hết cho 3 (NO)")
    ],
    "DRAGON-57": [
        ("999999937\n", "Số nguyên tố lớn (2 ước -> 1 cặp)"),
        ("720720\n", "Số có cực nhiều ước số")
    ],
    "DRAGON-58": [
        ("999999999\n", "Số lẻ lớn nhất"),
        ("987654320\n", "Số chẵn lớn nhất")
    ],
    "DRAGON-59": [
        ("999999937\n", "Số nguyên tố lớn (tổng tối thiểu 1 + n)"),
        ("987654320\n", "Số lớn tìm thừa số sát căn")
    ],
    "DRAGON-60": [
        ("99999\n", "Tìm số nguyên tố lớn nhất <= 99999"),
        ("88888\n", "Tìm số nguyên tố lớn nhất <= 88888")
    ],
    "DRAGON-61": [
        ("38\n", "Fibonacci thứ 38"),
        ("39\n", "Fibonacci thứ 39")
    ],
    "DRAGON-62": [
        ("99999\n", "Fibonacci lớn nhất <= 99999"),
        ("50000\n", "Fibonacci lớn nhất <= 50000")
    ],
    "DRAGON-63": [
        ("102334155\n", "Kiểm tra số Fibo 40 (YES)"),
        ("999999999\n", "Kiểm tra số lớn không thuộc Fibo (NO)")
    ],
    "DRAGON-64": [
        ("987654321\n", "Số 9 chữ số"),
        ("1000000000\n", "Số 10 chữ số (Biên 10^9)")
    ],
    "DRAGON-65": [
        ("987654321\n", "Tổng 9 chữ số khác nhau"),
        ("999999999\n", "Tổng 9 chữ số 9 (81)")
    ],
    "DRAGON-66": [
        ("987654321\n", "TBC 9 chữ số"),
        ("1000000000\n", "TBC số có nhiều số 0")
    ],
    "DRAGON-67": [
        ("500000000\n", "Số chữ số 0 tận cùng của 5.10^8!"),
        ("1000000000\n", "Số chữ số 0 tận cùng của 10^9!")
    ],
    "DRAGON-68": [
        ("10000\n", "Chữ số tận cùng khác 0 của 10000!"),
        ("50000\n", "Chữ số tận cùng khác 0 của 50000!")
    ],
    "DRAGON-69": [
        ("8\n100 200 -300 400 -500 600 700 800\n", "Tích các số tròn trăm (tận cùng 0)"),
        ("10\n11 13 17 19 21 23 27 29 31 33\n", "Tích nhiều số lẻ lớn")
    ],
    "DRAGON-70": [
        ("987654 123456\n", "Chữ số thứ 70 số lớn"),
        ("1 999999\n", "Chữ số thứ 70 mẫu số 999999")
    ],
    "DRAGON-71": [
        ("9999800001\n", "Chính phương lớn 99999^2 (YES)"),
        ("9999800002\n", "Không phải chính phương (NO)")
    ],
    "DRAGON-72": [
        ("88888\n", "Chính phương nhỏ nhất >= 88888"),
        ("99999\n", "Chính phương nhỏ nhất >= 99999")
    ],
    "DRAGON-73": [
        ("999999990\n", "Số may mắn lớn (YES)"),
        ("999999999\n", "Không phải số may mắn (NO)")
    ],
    "DRAGON-74": [
        ("888888888\n", "Đếm chính phương <= 888888888"),
        ("999999999\n", "Đếm chính phương <= 999999999")
    ],
    "DRAGON-75": [
        ("50000\n", "Đếm số nguyên tố <= 50000"),
        ("100000\n", "Đếm số nguyên tố <= 100000 (Sàng lớn)")
    ],
    "DRAGON-76": [
        ("10\n1 4 9 16 25 36 49 64 81 100\n", "Dãy 10 số chính phương liên tiếp"),
        ("12\n10 20 30 40 50 60 70 80 90 100 121 144\n", "Hỗn hợp 12 số")
    ],
    "DRAGON-77": [
        ("10\n101 103 107 109 113 127 131 137 139 149\n", "Dãy 10 số nguyên tố lớn"),
        ("15\n2 4 6 8 10 12 14 16 18 20 22 24 26 28 30\n", "Dãy 15 số chẵn (chỉ có 2 là NT)")
    ],
    "DRAGON-78": [
        ("10\n102 108 110 111 112 114 117 120 126 132\n", "Dãy 10 số Harshad lớn"),
        ("8\n101 103 107 109 113 127 131 137\n", "Dãy số nguyên tố không chia hết cho tổng CS")
    ],
    "DRAGON-79": [
        ("999983\n", "Tổng ước số nguyên tố lớn (chỉ 1 và chính nó)"),
        ("720720\n", "Tổng ước số phong phú lớn")
    ],
    "DRAGON-80": [
        ("79999\n", "Gần 80000 giây"),
        ("43200\n", "Nửa ngày (12:00:00)")
    ],
    "DRAGON-81": [
        ("9999 8888\n", "Ghép số 4 chữ số"),
        ("1000 2000\n", "Ghép số có nhiều số 0")
    ],
    "DRAGON-82": [
        ("10000 20000 1000000007\n", "Đoạn 10000 phần tử modulo lớn"),
        ("50000 60000 998244353\n", "Đoạn 10000 phần tử modulo chuẩn tin học")
    ],
    "DRAGON-83": [
        ("10\n100 200 300 400 500 600 700 800 900 1000\n", "Trọng số dãy cấp số cộng"),
        ("8\n10000 20000 30000 40000 50000 60000 70000 80000\n", "Trọng số mảng số lớn")
    ],
    "DRAGON-84": [
        ("9999\n", "Chuyển số thập phân 9999 sang nhị phân"),
        ("8192\n", "Lũy thừa đúng 2^13 (10000000000000)")
    ],
    "DRAGON-85": [
        ("101010101010101010101010101010\n", "Chuỗi nhị phân 30 bit đan xen"),
        ("11111111111111111111111111111111\n", "32 bit 1 (4294967295)")
    ],
    "DRAGON-86": [
        ("12\n1 2 3 4 5 15 10 5 8 7 6 9\n", "Chia băng số tổng 75"),
        ("10\n10 10 10 10 10 10 10 10 10 10\n", "10 phần tử bằng nhau (k = 10)")
    ],
    "DRAGON-87": [
        ("18\n", "Xâu Fibonacci thứ 18 (2584 ký tự)"),
        ("19\n", "Xâu Fibonacci thứ 19 (4181 ký tự)")
    ],
    "DRAGON-88": [
        ("16\n1 1 1 2 2 2 2 2 3 3 3 3 3 3 3 4\n", "Đoạn 7 số 3 liên tiếp"),
        ("10\n9 9 9 9 9 9 9 9 9 9\n", "Toàn bộ mảng bằng nhau (độ dài 10)")
    ],
    "DRAGON-89": [
        ("14\n-1 2 3 4 5 6 -2 7 8 9 10 -3 11 12\n", "Đoạn dương dài nhất 5 phần tử"),
        ("10\n1 2 3 4 5 6 7 8 9 10\n", "Toàn bộ là số dương (độ dài 10)")
    ],
    "DRAGON-90": [
        ("12\n1 3 5 7 9 11 10 8 6 4 2 0\n", "Dãy tăng dài rồi giảm dài"),
        ("8\n10 20 30 40 50 60 70 80\n", "Tăng nghiêm ngặt 8 phần tử")
    ],
    "DRAGON-91": [
        ("12\n1 -2 3 -4 5 -6 7 -8 9 -10 11 -12\n", "Đan xen hoàn hảo 12 phần tử"),
        ("10\n1 2 -3 4 -5 6 -7 8 9 10\n", "Đan xen ở đoạn giữa")
    ],
    "DRAGON-92": [
        ("12 5\n1 2 5 10 15 20 25 30 3 4 50 60\n", "Đoạn 6 phần tử chia hết cho 5"),
        ("10 7\n7 14 21 28 35 42 49 56 63 70\n", "Toàn bộ chia hết cho 7 (độ dài 10)")
    ],
    "DRAGON-93": [
        ("9999\n", "Phân số x = 9999"),
        ("5000\n", "Phân số x = 5000")
    ],
    "DRAGON-94": [
        ("9\n", "Tam giác Pascal bậc 9"),
        ("10\n", "Tam giác Pascal bậc 10 (giới hạn tối đa)")
    ],
    "DRAGON-95": [
        ("500000\n", "Phân tích 500000 thành tổng liên tiếp"),
        ("1000000\n", "Phân tích 10^6 thành tổng liên tiếp")
    ],
    "DRAGON-96": [
        ("4 4\n1 2 3 4\n5 6 7 8\n9 10 11 12\n13 14 15 16\n", "Ma trận tăng dần (chỉ có (3,0) là yên ngựa: min hàng 3 là 13, max cột 0 là 13)"),
        ("3 3\n7 7 7\n7 7 7\n7 7 7\n", "Ma trận toàn 7 (tất cả 9 phần tử là yên ngựa)")
    ],
    "DRAGON-97": [
        ("10\n98765432109876543210\n", "Xóa 10 số tạo số lớn nhất"),
        ("15\n1234567890123456789012345\n", "Xóa 15 số từ chuỗi 25 số")
    ],
    "DRAGON-98": [
        ("10\n98765432109876543210\n", "Xóa 10 số tạo số nhỏ nhất"),
        ("15\n9876543210987654321098765\n", "Xóa 15 số từ chuỗi 25 số")
    ],
    "DRAGON-99": [
        ("3 4\n12 11 10 9\n8 7 6 5\n4 3 2 1\n", "Ma trận 3x4 sắp xếp xoắn ốc"),
        ("2 5\n10 9 8 7 6\n5 4 3 2 1\n", "Ma trận 2x5 sắp xếp xoắn ốc")
    ],
    "DRAGON-100": [
        ("12 2\n1 1 1 1 1 1 1 1 1 1 1 1\n", "12 phần tử bằng 1 chia tỉ lệ 1:2 (4 và 8)"),
        ("10 4\n2 2 2 2 8 8 8 8 8 8\n", "Chia mảng tỉ lệ 1:4")
    ]
}

upgraded_count = 0

for p in problems:
    pid = p['id']
    num = int(pid.split('-')[1])
    # Upgrade problems from 50 to 100
    if 50 <= num <= 100 and pid in special_inputs:
        curr_tests = p.get('test_cases', [])
        # We want exactly 7 test cases
        if len(curr_tests) == 5:
            code = p['solution_python']
            inputs = special_inputs[pid]
            
            # Test 6
            out6 = run_py_solution(code, inputs[0][0])
            test6 = {
                "test_index": 6,
                "is_sample": False,
                "description": inputs[0][1],
                "input_data": inputs[0][0],
                "expected_output": out6
            }
            
            # Test 7
            out7 = run_py_solution(code, inputs[1][0])
            test7 = {
                "test_index": 7,
                "is_sample": False,
                "description": inputs[1][1],
                "input_data": inputs[1][0],
                "expected_output": out7
            }
            
            p['test_cases'].append(test6)
            p['test_cases'].append(test7)
            upgraded_count += 1
            print(f"Upgraded {pid} to 7 test cases!")

print(f"\nTotal upgraded problems: {upgraded_count}/51")

# Save back to data/problems.json
with open('data/problems.json', 'w', encoding='utf-8') as f:
    json.dump({"problems": problems}, f, ensure_ascii=False, indent=2)

print("Saved updated problems.json!")

# Re-seed SQLite database
from models.database import init_db, seed_problems_from_json, get_test_cases
seed_problems_from_json()

sample_tc = get_test_cases("DRAGON-50")
print(f"Verified DRAGON-50 in DB: {len(sample_tc)} test cases!")
