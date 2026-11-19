# Generator for problems DRAGON-50 through DRAGON-69
import json
import build_problems

existing_dict = {p['id']: p for p in build_problems.problems}

def get_starter_py(title=""):
    return f"""# Bí kíp luyện rồng - {title}
import sys

def solve():
    # Nhập dữ liệu và viết thuật toán của bạn tại đây
    pass

if __name__ == '__main__':
    solve()
"""

def get_starter_c(title=""):
    return f"""// Bí kíp luyện rồng - {title}
#include <stdio.h>

int main() {{
    // Khai báo biến, nhập dữ liệu và viết thuật toán tại đây
    
    return 0;
}}
"""

chunk_50_69 = []

# 50 - 56 from existing
for pid in [f'DRAGON-{i}' for i in range(50, 57)]:
    chunk_50_69.append(existing_dict[pid])

# 57: PHÂN TÍCH #4
chunk_50_69.append({
    "id": "DRAGON-57",
    "title": "Phân Tích #4 (Số Cách Phân Tích Tích)",
    "chapter": "Phần V. Bài toán phân tích & Số học",
    "difficulty": "Trung bình",
    "time_limit": 1.5,
    "memory_limit": 256,
    "description": "Nhập vào một số nguyên dương $n$. Hãy đếm số cách phân tích số $n$ thành tích của hai số nguyên dương $a$ và $b$ sao cho $a \\le b$ (các cặp $(a, b)$ và $(b, a)$ được coi là một cách giống nhau).",
    "input_format": "Một dòng duy nhất chứa số nguyên dương $n$ ($1 \\le n \\le 10^9$).",
    "output_format": "In ra một số nguyên là số cách phân tích tìm được.",
    "constraints": "$1 \\le n \\le 10^9$\nThời gian chạy: 1.5s\nBộ nhớ: 256MB",
    "sample_input": "6",
    "sample_output": "2",
    "hints": "Mỗi cặp $(a, b)$ tương ứng với một ước số $a \\le \\sqrt{n}$. Lặp $a$ từ 1 đến $\\lfloor\\sqrt{n}\\rfloor$ và kiểm tra $n \\% a == 0$.",
    "python_starter": get_starter_py("Phân Tích #4"),
    "c_starter": get_starter_c("Phân Tích #4"),
    "solution_python": """import sys
import math

def solve():
    line = sys.stdin.read().strip()
    if not line:
        return
    n = int(line)
    count = 0
    limit = math.isqrt(n)
    for a in range(1, limit + 1):
        if n % a == 0:
            count += 1
    print(count)

if __name__ == '__main__':
    solve()""",
    "solution_c": """#include <stdio.h>
#include <math.h>

int main() {
    long long n;
    if (scanf("%lld", &n) == 1) {
        long long count = 0;
        long long limit = (long long)sqrt(n);
        for (long long a = 1; a <= limit; a++) {
            if (n % a == 0) {
                count++;
            }
        }
        printf("%lld\\n", count);
    }
    return 0;
}""",
    "editorial": "### Phân Tích & Hướng Dẫn Giải\n- **Ý tưởng:** Cần tìm số cặp $(a, b)$ nguyên dương thỏa mãn $a \\times b = n$ và $a \\le b$. Vì $a \\le b$, ta suy ra $a \\le \\sqrt{n}$. Số lượng cặp $(a, b)$ chính bằng số ước số $a$ của $n$ thỏa mãn $a \\le \\sqrt{n}$.\n- **Độ phức tạp:** Thời gian $O(\\sqrt{n})$ (với $n \\le 10^9$, $\\sqrt{n} \\le 31622$ vòng lặp chạy cực nhanh trong vài ms). Bộ nhớ $O(1)$.",
    "test_cases": [
        {"test_index": 1, "is_sample": True, "description": "Test cơ bản (Mẫu)", "input_data": "6\n", "expected_output": "2\n"},
        {"test_index": 2, "is_sample": True, "description": "Số có nhiều ước", "input_data": "12\n", "expected_output": "3\n"},
        {"test_index": 3, "is_sample": False, "description": "Test biên (n = 1)", "input_data": "1\n", "expected_output": "1\n"},
        {"test_index": 4, "is_sample": False, "description": "Số chính phương (n = 36)", "input_data": "36\n", "expected_output": "5\n"},
        {"test_index": 5, "is_sample": False, "description": "Stress test (n = 10^9)", "input_data": "1000000000\n", "expected_output": "50\n"}
    ]
})

# 58 from existing
chunk_50_69.append(existing_dict["DRAGON-58"])

# 59: PHÂN TÍCH #6
chunk_50_69.append({
    "id": "DRAGON-59",
    "title": "Phân Tích #6 (Tổng Thừa Số Tối Thiểu)",
    "chapter": "Phần V. Bài toán phân tích & Số học",
    "difficulty": "Trung bình",
    "time_limit": 1.5,
    "memory_limit": 256,
    "description": "Nhập vào một số nguyên dương $n$. Tìm cách phân tích số $n$ thành tích hai số nguyên dương $a \\times b = n$ ($a \\le b$) sao cho tổng hai số $a + b$ là nhỏ nhất (tức hai thừa số gần nhau nhất, như ví dụ trong sách: $6 \\to 2\\ 3$).",
    "input_format": "Một dòng duy nhất chứa số nguyên dương $n$ ($1 \\le n \\le 10^9$).",
    "output_format": "In ra 2 số nguyên dương $a$ và $b$ ($a \\le b$), cách nhau bởi một khoảng trắng.",
    "constraints": "$1 \\le n \\le 10^9$\nThời gian chạy: 1.5s\nBộ nhớ: 256MB",
    "sample_input": "6",
    "sample_output": "2 3",
    "hints": "Cho $a$ chạy lùi từ $\\lfloor\\sqrt{n}\\rfloor$ về 1. Ước $a$ đầu tiên tìm được thỏa mãn $n \\% a == 0$ chính là thừa số lớn nhất $\\le \\sqrt{n}$, cho tổng $a + b$ nhỏ nhất.",
    "python_starter": get_starter_py("Phân Tích #6"),
    "c_starter": get_starter_c("Phân Tích #6"),
    "solution_python": """import sys
import math

def solve():
    line = sys.stdin.read().strip()
    if not line:
        return
    n = int(line)
    start = math.isqrt(n)
    for a in range(start, 0, -1):
        if n % a == 0:
            b = n // a
            print(f"{a} {b}")
            return

if __name__ == '__main__':
    solve()""",
    "solution_c": """#include <stdio.h>
#include <math.h>

int main() {
    long long n;
    if (scanf("%lld", &n) == 1) {
        long long start = (long long)sqrt(n);
        for (long long a = start; a >= 1; a--) {
            if (n % a == 0) {
                long long b = n / a;
                printf("%lld %lld\\n", a, b);
                return 0;
            }
        }
    }
    return 0;
}""",
    "editorial": "### Phân Tích & Hướng Dẫn Giải\n- **Ý tưởng:** Với tích $a \\times b = n$ cố định, tổng $a + b$ đạt giá trị nhỏ nhất khi $a$ và $b$ gần nhau nhất (tức hiệu $b - a$ nhỏ nhất). Vì $a \\le \\sqrt{n} \\le b$, ta bắt đầu duyệt $a$ từ $\\lfloor\\sqrt{n}\\rfloor$ giảm dần về 1. Ước số $a$ đầu tiên chia hết cho $n$ sẽ cho $a$ lớn nhất có thể và $b = n / a$ nhỏ nhất có thể, tức tổng $a + b$ nhỏ nhất.\n- **Độ phức tạp:** Thời gian $O(\\sqrt{n})$, Bộ nhớ $O(1)$.",
    "test_cases": [
        {"test_index": 1, "is_sample": True, "description": "Test cơ bản (Mẫu)", "input_data": "6\n", "expected_output": "2 3\n"},
        {"test_index": 2, "is_sample": True, "description": "Số chính phương", "input_data": "16\n", "expected_output": "4 4\n"},
        {"test_index": 3, "is_sample": False, "description": "Test biên (n = 1)", "input_data": "1\n", "expected_output": "1 1\n"},
        {"test_index": 4, "is_sample": False, "description": "Số nguyên tố (n = 13)", "input_data": "13\n", "expected_output": "1 13\n"},
        {"test_index": 5, "is_sample": False, "description": "Stress test (n = 10^9)", "input_data": "1000000000\n", "expected_output": "31250 32000\n"}
    ]
})

# 60 from existing
chunk_50_69.append(existing_dict["DRAGON-60"])

# 61: FIBONACCI #1
chunk_50_69.append({
    "id": "DRAGON-61",
    "title": "Fibonacci #1 (Số Fibonacci Thứ N)",
    "chapter": "Phần VI. Dãy số & Đệ quy cơ bản",
    "difficulty": "Dễ",
    "time_limit": 1.5,
    "memory_limit": 256,
    "description": "Dãy số Fibonacci được định nghĩa như sau: $f(1) = 1, f(2) = 1, f(i) = f(i-1) + f(i-2)$ với mọi $i \\ge 3$.\n\nNhập vào một số nguyên dương $n$. Hãy in ra số Fibonacci thứ $n$.",
    "input_format": "Một dòng duy nhất chứa số nguyên dương $n$ ($1 \\le n \\le 40$).",
    "output_format": "In ra số Fibonacci thứ $n$.",
    "constraints": "$1 \\le n \\le 40$\nThời gian chạy: 1.5s\nBộ nhớ: 256MB",
    "sample_input": "6",
    "sample_output": "8",
    "hints": "Sử dụng mảng hoặc 2 biến để tính tịnh tiến dãy Fibonacci từ $f(1), f(2)$ lên $f(n)$.",
    "python_starter": get_starter_py("Fibonacci #1"),
    "c_starter": get_starter_c("Fibonacci #1"),
    "solution_python": """import sys

def solve():
    line = sys.stdin.read().strip()
    if not line:
        return
    n = int(line)
    if n <= 2:
        print(1)
        return
    a, b = 1, 1
    for _ in range(3, n + 1):
        a, b = b, a + b
    print(b)

if __name__ == '__main__':
    solve()""",
    "solution_c": """#include <stdio.h>

int main() {
    int n;
    if (scanf("%d", &n) == 1) {
        if (n <= 2) {
            printf("1\\n");
            return 0;
        }
        long long a = 1, b = 1;
        for (int i = 3; i <= n; i++) {
            long long next = a + b;
            a = b;
            b = next;
        }
        printf("%lld\\n", b);
    }
    return 0;
}""",
    "editorial": "### Phân Tích & Hướng Dẫn Giải\n- **Ý tưởng:** Với $n \\le 40$, giá trị $f(40) = 102334155$ hoàn toàn nằm vừa trong kiểu số nguyên 32-bit (và 64-bit `long long` trong C). Duyệt vòng lặp từ 3 đến $n$ với 2 biến lưu $f(i-2)$ và $f(i-1)$ để cập nhật trong thời gian $O(n)$ và bộ nhớ $O(1)$.\n- **Độ phức tạp:** Thời gian $O(n)$, Bộ nhớ $O(1)$.",
    "test_cases": [
        {"test_index": 1, "is_sample": True, "description": "Test cơ bản (Mẫu)", "input_data": "6\n", "expected_output": "8\n"},
        {"test_index": 2, "is_sample": True, "description": "Test n = 1", "input_data": "1\n", "expected_output": "1\n"},
        {"test_index": 3, "is_sample": False, "description": "Test n = 2", "input_data": "2\n", "expected_output": "1\n"},
        {"test_index": 4, "is_sample": False, "description": "Test n = 10", "input_data": "10\n", "expected_output": "55\n"},
        {"test_index": 5, "is_sample": False, "description": "Biên trên (n = 40)", "input_data": "40\n", "expected_output": "102334155\n"}
    ]
})

# 62: FIBONACCI #2
chunk_50_69.append({
    "id": "DRAGON-62",
    "title": "Fibonacci #2 (Fibonacci Lớn Nhất Nhỏ Hơn Hoặc Bằng N)",
    "chapter": "Phần VI. Dãy số & Đệ quy cơ bản",
    "difficulty": "Dễ",
    "time_limit": 1.5,
    "memory_limit": 256,
    "description": "Nhập vào một số nguyên dương $n$. Hãy in ra số Fibonacci lớn nhất nhỏ hơn hoặc bằng $n$. Dãy Fibonacci được định nghĩa: $f(1) = 1, f(2) = 1, f(i) = f(i-1) + f(i-2)$.",
    "input_format": "Một dòng duy nhất chứa số nguyên dương $n$ ($1 \\le n \\le 100000$).",
    "output_format": "In ra một số nguyên là số Fibonacci lớn nhất $\\le n$.",
    "constraints": "$1 \\le n \\le 100000$\nThời gian chạy: 1.5s\nBộ nhớ: 256MB",
    "sample_input": "6",
    "sample_output": "5",
    "hints": "Sinh liên tiếp các số Fibonacci $1, 1, 2, 3, 5, 8, ...$ chừng nào số tiếp theo còn $\\le n$.",
    "python_starter": get_starter_py("Fibonacci #2"),
    "c_starter": get_starter_c("Fibonacci #2"),
    "solution_python": """import sys

def solve():
    line = sys.stdin.read().strip()
    if not line:
        return
    n = int(line)
    a, b = 1, 1
    while True:
        c = a + b
        if c > n:
            break
        a, b = b, c
    print(b if n >= 1 else 0)

if __name__ == '__main__':
    solve()""",
    "solution_c": """#include <stdio.h>

int main() {
    long long n;
    if (scanf("%lld", &n) == 1) {
        long long a = 1, b = 1;
        while (1) {
            long long c = a + b;
            if (c > n) break;
            a = b;
            b = c;
        }
        printf("%lld\\n", b);
    }
    return 0;
}""",
    "editorial": "### Phân Tích & Hướng Dẫn Giải\n- **Ý tưởng:** Bắt đầu với $a = 1, b = 1$. Ở mỗi bước, tính $c = a + b$. Nếu $c \\le n$, cập nhật $a = b, b = c$. Khi $c > n$, vòng lặp dừng lại và giá trị $b$ chính là số Fibonacci lớn nhất $\\le n$.\n- **Độ phức tạp:** Thời gian $O(\\log n)$, Bộ nhớ $O(1)$.",
    "test_cases": [
        {"test_index": 1, "is_sample": True, "description": "Test cơ bản (Mẫu)", "input_data": "6\n", "expected_output": "5\n"},
        {"test_index": 2, "is_sample": True, "description": "Test n = 1", "input_data": "1\n", "expected_output": "1\n"},
        {"test_index": 3, "is_sample": False, "description": "Số đúng bằng số Fibonacci (n = 8)", "input_data": "8\n", "expected_output": "8\n"},
        {"test_index": 4, "is_sample": False, "description": "Test n = 100", "input_data": "100\n", "expected_output": "89\n"},
        {"test_index": 5, "is_sample": False, "description": "Biên trên (n = 100000)", "input_data": "100000\n", "expected_output": "75025\n"}
    ]
})

# 63: FIBONACCI #3
chunk_50_69.append({
    "id": "DRAGON-63",
    "title": "Fibonacci #3 (Kiểm Tra Số Fibonacci)",
    "chapter": "Phần VI. Dãy số & Đệ quy cơ bản",
    "difficulty": "Dễ",
    "time_limit": 1.5,
    "memory_limit": 256,
    "description": "Nhập vào một số nguyên dương $n$. Kiểm tra xem $n$ có phải là số thuộc dãy Fibonacci hay không. Biết dãy Fibonacci có $f(1)=1, f(2)=1, f(i)=f(i-1)+f(i-2)$.",
    "input_format": "Một dòng duy nhất chứa số nguyên dương $n$ ($1 \\le n \\le 10^9$).",
    "output_format": "In ra 'YES' nếu $n$ là một số Fibonacci, ngược lại in ra 'NO'.",
    "constraints": "$1 \\le n \\le 10^9$\nThời gian chạy: 1.5s\nBộ nhớ: 256MB",
    "sample_input": "3",
    "sample_output": "YES",
    "hints": "Dãy Fibonacci tăng theo hàm mũ, số Fibonacci $\\le 10^9$ chỉ có khoảng 45 số. Ta có thể sinh dần các số Fibonacci cho đến khi bằng $n$ (YES) hoặc vượt quá $n$ (NO).",
    "python_starter": get_starter_py("Fibonacci #3"),
    "c_starter": get_starter_c("Fibonacci #3"),
    "solution_python": """import sys

def solve():
    line = sys.stdin.read().strip()
    if not line:
        return
    n = int(line)
    if n == 1:
        print("YES")
        return
    a, b = 1, 1
    while b < n:
        a, b = b, a + b
    if b == n:
        print("YES")
    else:
        print("NO")

if __name__ == '__main__':
    solve()""",
    "solution_c": """#include <stdio.h>

int main() {
    long long n;
    if (scanf("%lld", &n) == 1) {
        if (n == 1) {
            printf("YES\\n");
            return 0;
        }
        long long a = 1, b = 1;
        while (b < n) {
            long long c = a + b;
            a = b;
            b = c;
        }
        if (b == n) {
            printf("YES\\n");
        } else {
            printf("NO\\n");
        }
    }
    return 0;
}""",
    "editorial": "### Phân Tích & Hướng Dẫn Giải\n- **Ý tưởng:** Ta sinh tuần tự các phần tử của dãy Fibonacci xuất phát từ $f(1)=1, f(2)=1$. Chừng nào số hiện tại $b < n$, ta tiếp tục cộng số tiếp theo. Nếu dừng lại tại $b == n$ thì kết luận 'YES', ngược lại nếu $b > n$ thì 'NO'.\n- **Độ phức tạp:** Thời gian $O(\\log n)$ (tối đa ~50 bước lặp), Bộ nhớ $O(1)$.",
    "test_cases": [
        {"test_index": 1, "is_sample": True, "description": "Test cơ bản (Mẫu 1)", "input_data": "3\n", "expected_output": "YES\n"},
        {"test_index": 2, "is_sample": True, "description": "Test không phải Fibo (Mẫu 2)", "input_data": "9\n", "expected_output": "NO\n"},
        {"test_index": 3, "is_sample": False, "description": "Test n = 1", "input_data": "1\n", "expected_output": "YES\n"},
        {"test_index": 4, "is_sample": False, "description": "Fibo lớn (n = 55)", "input_data": "55\n", "expected_output": "YES\n"},
        {"test_index": 5, "is_sample": False, "description": "Số lớn không phải Fibo", "input_data": "1000000000\n", "expected_output": "NO\n"}
    ]
})

# 64, 65 from existing
chunk_50_69.append(existing_dict["DRAGON-64"])
chunk_50_69.append(existing_dict["DRAGON-65"])

# 66: TRUNG BÌNH CỘNG
chunk_50_69.append({
    "id": "DRAGON-66",
    "title": "Trung Bình Cộng Chữ Số",
    "chapter": "Phần VII. Xử lý chữ số",
    "difficulty": "Dễ",
    "time_limit": 1.5,
    "memory_limit": 256,
    "description": "Nhập vào một số nguyên dương $n$. Hãy tính và in ra trung bình cộng các chữ số của $n$. Kết quả được làm tròn đến đúng 2 chữ số thập phân.",
    "input_format": "Một dòng duy nhất chứa số nguyên dương $n$ ($1 \\le n \\le 10^9$).",
    "output_format": "In ra giá trị trung bình cộng làm tròn đến 2 chữ số thập phân (định dạng `%.2f`).",
    "constraints": "$1 \\le n \\le 10^9$\nThời gian chạy: 1.5s\nBộ nhớ: 256MB",
    "sample_input": "346",
    "sample_output": "4.33",
    "hints": "Tách từng chữ số của $n$ qua phép chia dư $n \\% 10$ và chia nguyên $n // 10$, tính tổng và đếm số lượng chữ số, sau đó chia lấy trung bình.",
    "python_starter": get_starter_py("Trung Bình Cộng Chữ Số"),
    "c_starter": get_starter_c("Trung Bình Cộng Chữ Số"),
    "solution_python": """import sys

def solve():
    line = sys.stdin.read().strip()
    if not line:
        return
    digits = [int(c) for c in line if c.isdigit()]
    if digits:
        avg = sum(digits) / len(digits)
        print(f"{avg:.2f}")

if __name__ == '__main__':
    solve()""",
    "solution_c": """#include <stdio.h>

int main() {
    long long n;
    if (scanf("%lld", &n) == 1) {
        long long sum = 0;
        int count = 0;
        while (n > 0) {
            sum += (n % 10);
            count++;
            n /= 10;
        }
        double avg = (double)sum / count;
        printf("%.2f\\n", avg);
    }
    return 0;
}""",
    "editorial": "### Phân Tích & Hướng Dẫn Giải\n- **Ý tưởng:** Đọc số nguyên $n$. Dùng vòng lặp lấy từng chữ số bằng `n % 10`, cộng vào biến `sum` và tăng biến `count`. Sau khi xử lý hết chữ số, in kết quả `(double)sum / count` với định dạng `%.2f`.\n- **Độ phức tạp:** Thời gian $O(\\log_{10} n)$, Bộ nhớ $O(1)$.",
    "test_cases": [
        {"test_index": 1, "is_sample": True, "description": "Test cơ bản (Mẫu)", "input_data": "346\n", "expected_output": "4.33\n"},
        {"test_index": 2, "is_sample": True, "description": "Số có chữ số 0", "input_data": "100\n", "expected_output": "0.33\n"},
        {"test_index": 3, "is_sample": False, "description": "Số có 1 chữ số", "input_data": "9\n", "expected_output": "9.00\n"},
        {"test_index": 4, "is_sample": False, "description": "Các chữ số giống nhau", "input_data": "5555\n", "expected_output": "5.00\n"},
        {"test_index": 5, "is_sample": False, "description": "Số đầy đủ 1 đến 9", "input_data": "123456789\n", "expected_output": "5.00\n"}
    ]
})

# 67 from existing
chunk_50_69.append(existing_dict["DRAGON-67"])

# 68: TẬN CÙNG (KHÓ)
chunk_50_69.append({
    "id": "DRAGON-68",
    "title": "Tận Cùng (Khó) - Chữ Số Khác 0 Cuối Cùng Của N!",
    "chapter": "Phần VII. Xử lý chữ số",
    "difficulty": "Khó",
    "time_limit": 1.5,
    "memory_limit": 256,
    "description": "Nhập vào một số nguyên dương $n$. Hãy tìm và in ra chữ số tận cùng khác 0 của $n!$ ($n! = 1 \\times 2 \\times 3 \\times \\dots \\times n$).",
    "input_format": "Một dòng duy nhất chứa số nguyên dương $n$ ($1 \\le n \\le 100000$).",
    "output_format": "In ra một chữ số duy nhất là chữ số khác 0 tận cùng của $n!$.",
    "constraints": "$1 \\le n \\le 100000$\nThời gian chạy: 1.5s\nBộ nhớ: 256MB",
    "sample_input": "10",
    "sample_output": "8",
    "hints": "Các số 0 tận cùng được tạo thành bởi tích $2 \\times 5$. Ta đếm số thừa số 2 và 5 rồi triệt tiêu chúng. Phần thừa số 2 dư ra sẽ nhân theo modulo 10.",
    "python_starter": get_starter_py("Tận Cùng (Khó)"),
    "c_starter": get_starter_c("Tận Cùng (Khó)"),
    "solution_python": """import sys

def solve():
    line = sys.stdin.read().strip()
    if not line:
        return
    n = int(line)
    if n <= 1:
        print(1)
        return
    ans = 1
    c2 = 0
    c5 = 0
    for i in range(1, n + 1):
        cur = i
        while cur % 2 == 0:
            c2 += 1
            cur //= 2
        while cur % 5 == 0:
            c5 += 1
            cur //= 5
        ans = (ans * (cur % 10)) % 10
    rem2 = c2 - c5
    ans = (ans * pow(2, rem2, 10)) % 10
    print(ans)

if __name__ == '__main__':
    solve()""",
    "solution_c": """#include <stdio.h>

int main() {
    int n;
    if (scanf("%d", &n) == 1) {
        if (n <= 1) {
            printf("1\\n");
            return 0;
        }
        int ans = 1;
        int c2 = 0, c5 = 0;
        for (int i = 1; i <= n; i++) {
            int cur = i;
            while (cur % 2 == 0) {
                c2++;
                cur /= 2;
            }
            while (cur % 5 == 0) {
                c5++;
                cur /= 5;
            }
            ans = (ans * (cur % 10)) % 10;
        }
        int rem2 = c2 - c5;
        for (int i = 0; i < rem2; i++) {
            ans = (ans * 2) % 10;
        }
        printf("%d\\n", ans);
    }
    return 0;
}""",
    "editorial": "### Phân Tích & Hướng Dẫn Giải\n- **Ý tưởng:** Mọi chữ số 0 tận cùng đều xuất phát từ việc nhân thừa số nguyên tố 2 và 5 ($2 \\times 5 = 10$). Do đó, ta phân tích mỗi số từ 1 đến $n$: rút hết thừa số 2 và thừa số 5, đồng thời nhân các phần còn lại theo modulo 10.\n- Vì số lượng thừa số 2 trong $n!$ luôn nhiều hơn số thừa số 5, sau khi ghép cặp triệt tiêu sẽ còn dư lại $(c2 - c5)$ thừa số 2. Ta chỉ cần nhân thêm $2^{(c2 - c5)} \\pmod{10}$ vào kết quả cuối cùng.\n- **Độ phức tạp:** Thời gian $O(n \\log n)$, Bộ nhớ $O(1)$.",
    "test_cases": [
        {"test_index": 1, "is_sample": True, "description": "Test cơ bản (Mẫu n = 10)", "input_data": "10\n", "expected_output": "8\n"},
        {"test_index": 2, "is_sample": True, "description": "Test nhỏ n = 5 (5! = 120)", "input_data": "5\n", "expected_output": "2\n"},
        {"test_index": 3, "is_sample": False, "description": "Test biên n = 1", "input_data": "1\n", "expected_output": "1\n"},
        {"test_index": 4, "is_sample": False, "description": "Test n = 20", "input_data": "20\n", "expected_output": "4\n"},
        {"test_index": 5, "is_sample": False, "description": "Stress test n = 100", "input_data": "100\n", "expected_output": "4\n"}
    ]
})

# 69: CHỮ SỐ TẬN CÙNG
chunk_50_69.append({
    "id": "DRAGON-69",
    "title": "Chữ Số Tận Cùng Của Tích Mảng",
    "chapter": "Phần VIII. Mảng một chiều cơ bản",
    "difficulty": "Dễ",
    "time_limit": 1.5,
    "memory_limit": 256,
    "description": "Nhập vào dãy $A$ có $n$ phần tử. In ra chữ số tận cùng của tích các số trong dãy. Chữ số tận cùng luôn là một chữ số từ 0 đến 9.",
    "input_format": "Dòng 1: Số nguyên dương $n$ ($1 \\le n \\le 100$).\\nDòng 2: $n$ số nguyên $a_i$ ($-100000 \\le a_i \\le 100000$), cách nhau bởi dấu cách.",
    "output_format": "In ra chữ số tận cùng của tích tất cả các số trong dãy.",
    "constraints": "$1 \\le n \\le 100$\\n$-100000 \\le a_i \\le 100000$\\nThời gian chạy: 1.5s\\nBộ nhớ: 256MB",
    "sample_input": "4\n1 -2 3 4",
    "sample_output": "4",
    "hints": "Chữ số tận cùng của tích chỉ phụ thuộc vào chữ số tận cùng của từng phần tử. Tích nhân dồn lấy modulo 10 trên giá trị tuyệt đối.",
    "python_starter": get_starter_py("Chữ Số Tận Cùng"),
    "c_starter": get_starter_c("Chữ Số Tận Cùng"),
    "solution_python": """import sys

def solve():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    nums = [int(x) for x in tokens[1:n+1]]
    prod = 1
    for x in nums:
        prod = (prod * abs(x)) % 10
    print(prod)

if __name__ == '__main__':
    solve()""",
    "solution_c": """#include <stdio.h>
#include <stdlib.h>

int main() {
    int n;
    if (scanf("%d", &n) == 1) {
        int prod = 1;
        for (int i = 0; i < n; i++) {
            long long x;
            if (scanf("%lld", &x) == 1) {
                prod = (prod * (abs(x) % 10)) % 10;
            }
        }
        printf("%d\\n", prod);
    }
    return 0;
}""",
    "editorial": "### Phân Tích & Hướng Dẫn Giải\n- **Ý tưởng:** Chữ số tận cùng của một số nguyên bằng giá trị tuyệt đối của số đó chia lấy dư cho 10. Để tránh tràn số khi nhân mảng, ta nhân dồn và lấy `abs(x) % 10` sau mỗi lượt.\n- **Độ phức tạp:** Thời gian $O(n)$, Bộ nhớ $O(1)$.",
    "test_cases": [
        {"test_index": 1, "is_sample": True, "description": "Test cơ bản (Mẫu)", "input_data": "4\n1 -2 3 4\n", "expected_output": "4\n"},
        {"test_index": 2, "is_sample": True, "description": "Tích có tận cùng là 0", "input_data": "3\n2 5 7\n", "expected_output": "0\n"},
        {"test_index": 3, "is_sample": False, "description": "Mảng có 1 phần tử âm", "input_data": "1\n-9\n", "expected_output": "9\n"},
        {"test_index": 4, "is_sample": False, "description": "Tất cả các số tận cùng là 1", "input_data": "5\n11 21 31 41 51\n", "expected_output": "1\n"},
        {"test_index": 5, "is_sample": False, "description": "Nhiều số âm đan xen", "input_data": "6\n-13 27 -33 49 51 -63\n", "expected_output": "1\n"}
    ]
})

with open('data_generators/problems_50_69.py', 'w', encoding='utf-8') as f:
    f.write('problems = ' + repr(chunk_50_69) + '\n')

print(f"Generated data_generators/problems_50_69.py with {len(chunk_50_69)} problems!")
