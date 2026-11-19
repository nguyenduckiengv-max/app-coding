# Generator for problems DRAGON-70 through DRAGON-85
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

chunk_70_85 = []

# 70: CHỮ SỐ THẬP PHÂN THỨ 70
chunk_70_85.append({
    "id": "DRAGON-70",
    "title": "Chữ Số Thập Phân Thứ 70",
    "chapter": "Phần VII. Xử lý chữ số",
    "difficulty": "Trung bình",
    "time_limit": 1.5,
    "memory_limit": 256,
    "description": "Nhập vào hai số nguyên dương $a$ và $b$. Hãy tìm và in ra chữ số thập phân thứ 70 sau dấu phẩy của phép chia $a / b$.",
    "input_format": "Một dòng duy nhất chứa hai số nguyên dương $a$ và $b$ ($1 \\le a, b \\le 10^6$), cách nhau bởi một khoảng trắng.",
    "output_format": "In ra một chữ số duy nhất (từ 0 đến 9).",
    "constraints": "$1 \\le a, b \\le 10^6$\\nThời gian chạy: 1.5s\\nBộ nhớ: 256MB",
    "sample_input": "10 3",
    "sample_output": "3",
    "hints": "Mô phỏng phép chia đặt tính tay: lấy phần dư $r = a \\% b$, lặp 70 lần: $r = r \\times 10$, chữ số $d = r // b$, sau đó cập nhật $r = r \\% b$.",
    "python_starter": get_starter_py("Chữ Số Thập Phân Thứ 70"),
    "c_starter": get_starter_c("Chữ Số Thập Phân Thứ 70"),
    "solution_python": """import sys

def solve():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    a, b = int(tokens[0]), int(tokens[1])
    r = a % b
    d = 0
    for _ in range(70):
        r *= 10
        d = r // b
        r %= b
    print(d)

if __name__ == '__main__':
    solve()""",
    "solution_c": """#include <stdio.h>

int main() {
    long long a, b;
    if (scanf("%lld %lld", &a, &b) == 2) {
        long long r = a % b;
        int d = 0;
        for (int i = 0; i < 70; i++) {
            r *= 10;
            d = r / b;
            r %= b;
        }
        printf("%d\\n", d);
    }
    return 0;
}""",
    "editorial": "### Phân Tích & Hướng Dẫn Giải\\n- **Ý tưởng:** Các kiểu dữ liệu số thực như `double` hay `float` chỉ có độ chính xác khoảng 15-17 chữ số thập phân nên không thể lưu trực tiếp đến chữ số thứ 70. Ta áp dụng phương pháp chia tay cơ bản ở tiểu học: sau phần nguyên, mỗi lần hạ một chữ số 0 tương ứng với $r = r \\times 10$, chữ số thương tiếp theo là $r // b$, và số dư mới là $r \\% b$. Lặp lại đúng 70 lần để thu được chữ số thập phân thứ 70.\\n- **Độ phức tạp:** Thời gian $O(1)$ (chỉ 70 bước), Bộ nhớ $O(1)$.",
    "test_cases": [
        {"test_index": 1, "is_sample": True, "description": "Test cơ bản (Mẫu 10/3)", "input_data": "10 3\n", "expected_output": "3\n"},
        {"test_index": 2, "is_sample": True, "description": "Phép chia hữu hạn (1/2 = 0.5000...)", "input_data": "1 2\n", "expected_output": "0\n"},
        {"test_index": 3, "is_sample": False, "description": "Phân số 1/7 có chu kỳ 6 (142857)", "input_data": "1 7\n", "expected_output": "8\n"},
        {"test_index": 4, "is_sample": False, "description": "Số Pi xấp xỉ 22/7", "input_data": "22 7\n", "expected_output": "8\n"},
        {"test_index": 5, "is_sample": False, "description": "Mẫu số lớn", "input_data": "355 113\n", "expected_output": "9\n"}
    ]
})

# 71 from existing
chunk_70_85.append(existing_dict["DRAGON-71"])

# 72: SỐ CHÍNH PHƯƠNG #2
chunk_70_85.append({
    "id": "DRAGON-72",
    "title": "Số Chính Phương #2 (Chính Phương Nhỏ Nhất >= N)",
    "chapter": "Phần V. Bài toán phân tích & Số học",
    "difficulty": "Dễ",
    "time_limit": 1.5,
    "memory_limit": 256,
    "description": "Nhập vào số nguyên dương $n$. In ra số chính phương nhỏ nhất lớn hơn hoặc bằng $n$. (Số chính phương là bình phương của một số nguyên).",
    "input_format": "Một dòng duy nhất chứa số nguyên $n$ ($0 \\le n \\le 100000$).",
    "output_format": "In ra số chính phương nhỏ nhất $\\ge n$.",
    "constraints": "$0 \\le n \\le 100000$\\nThời gian chạy: 1.5s\\nBộ nhớ: 256MB",
    "sample_input": "6",
    "sample_output": "9",
    "hints": "Tính căn bậc hai của $n$. Nếu căn bậc hai bình phương nhỏ hơn $n$, tăng lên 1 đơn vị rồi bình phương lại.",
    "python_starter": get_starter_py("Số Chính Phương #2"),
    "c_starter": get_starter_c("Số Chính Phương #2"),
    "solution_python": """import sys
import math

def solve():
    line = sys.stdin.read().strip()
    if not line:
        return
    n = int(line)
    if n <= 0:
        print(0)
        return
    k = math.isqrt(n)
    if k * k < n:
        k += 1
    print(k * k)

if __name__ == '__main__':
    solve()""",
    "solution_c": """#include <stdio.h>
#include <math.h>

int main() {
    long long n;
    if (scanf("%lld", &n) == 1) {
        if (n <= 0) {
            printf("0\\n");
            return 0;
        }
        long long k = (long long)sqrt(n);
        if (k * k < n) {
            k++;
        }
        printf("%lld\\n", k * k);
    }
    return 0;
}""",
    "editorial": "### Phân Tích & Hướng Dẫn Giải\\n- **Ý tưởng:** Với $n \\ge 0$, ta tính $k = \\lfloor\\sqrt{n}\\rfloor$. Nếu $k \\times k < n$, thì số chính phương nhỏ nhất $\\ge n$ chính là $(k + 1)^2$. Nếu $k \\times k == n$, thì kết quả chính là $k^2 = n$.\\n- **Độ phức tạp:** Thời gian $O(1)$, Bộ nhớ $O(1)$.",
    "test_cases": [
        {"test_index": 1, "is_sample": True, "description": "Test cơ bản (Mẫu n = 6)", "input_data": "6\n", "expected_output": "9\n"},
        {"test_index": 2, "is_sample": True, "description": "Bản thân n đã là số chính phương", "input_data": "16\n", "expected_output": "16\n"},
        {"test_index": 3, "is_sample": False, "description": "Test biên n = 0", "input_data": "0\n", "expected_output": "0\n"},
        {"test_index": 4, "is_sample": False, "description": "Test biên n = 1", "input_data": "1\n", "expected_output": "1\n"},
        {"test_index": 5, "is_sample": False, "description": "Biên trên n = 99999", "input_data": "99999\n", "expected_output": "100489\n"}
    ]
})

# 73 from existing
chunk_70_85.append(existing_dict["DRAGON-73"])

# 74: ĐẾM #1
chunk_70_85.append({
    "id": "DRAGON-74",
    "title": "Đếm #1 (Số Lượng Số Chính Phương <= N)",
    "chapter": "Phần V. Bài toán phân tích & Số học",
    "difficulty": "Dễ",
    "time_limit": 1.5,
    "memory_limit": 256,
    "description": "Nhập vào số nguyên dương $n$. Đếm xem có bao nhiêu số chính phương dương nhỏ hơn hoặc bằng $n$ (các số có dạng $k^2$ với $k \\ge 1, k^2 \\le n$).",
    "input_format": "Một dòng duy nhất chứa số nguyên dương $n$ ($1 \\le n \\le 10^9$).",
    "output_format": "In ra số lượng số chính phương $\\le n$.",
    "constraints": "$1 \\le n \\le 10^9$\\nThời gian chạy: 1.5s\\nBộ nhớ: 256MB",
    "sample_input": "10",
    "sample_output": "3",
    "hints": "Số các số chính phương $1^2, 2^2, \\dots, k^2 \\le n$ chính bằng $\\lfloor\\sqrt{n}\\rfloor$.",
    "python_starter": get_starter_py("Đếm #1"),
    "c_starter": get_starter_c("Đếm #1"),
    "solution_python": """import sys
import math

def solve():
    line = sys.stdin.read().strip()
    if not line:
        return
    n = int(line)
    print(math.isqrt(n))

if __name__ == '__main__':
    solve()""",
    "solution_c": """#include <stdio.h>
#include <math.h>

int main() {
    long long n;
    if (scanf("%lld", &n) == 1) {
        long long ans = (long long)sqrt(n);
        printf("%lld\\n", ans);
    }
    return 0;
}""",
    "editorial": "### Phân Tích & Hướng Dẫn Giải\\n- **Ý tưởng:** Các số chính phương dương nhỏ hơn hoặc bằng $n$ là $1^2, 2^2, 3^2, \\dots, k^2$ với $k^2 \\le n \\iff k \\le \\sqrt{n}$. Do đó số lượng số chính phương cần tìm chính là phần nguyên của căn bậc hai của $n$, tức $\\lfloor\\sqrt{n}\\rfloor$.\\n- **Độ phức tạp:** Thời gian $O(1)$, Bộ nhớ $O(1)$.",
    "test_cases": [
        {"test_index": 1, "is_sample": True, "description": "Test cơ bản (Mẫu n = 10)", "input_data": "10\n", "expected_output": "3\n"},
        {"test_index": 2, "is_sample": True, "description": "Test n = 1", "input_data": "1\n", "expected_output": "1\n"},
        {"test_index": 3, "is_sample": False, "description": "Số chính phương (n = 25)", "input_data": "25\n", "expected_output": "5\n"},
        {"test_index": 4, "is_sample": False, "description": "Gần chính phương (n = 99)", "input_data": "99\n", "expected_output": "9\n"},
        {"test_index": 5, "is_sample": False, "description": "Stress test n = 10^9", "input_data": "1000000000\n", "expected_output": "31622\n"}
    ]
})

# 75: ĐẾM #2
chunk_70_85.append({
    "id": "DRAGON-75",
    "title": "Đếm #2 (Số Lượng Số Nguyên Tố <= N)",
    "chapter": "Phần V. Bài toán phân tích & Số học",
    "difficulty": "Trung bình",
    "time_limit": 1.5,
    "memory_limit": 256,
    "description": "Nhập vào số nguyên dương $n$. Đếm xem có bao nhiêu số nguyên tố nhỏ hơn hoặc bằng $n$.",
    "input_format": "Một dòng duy nhất chứa số nguyên dương $n$ ($1 \\le n \\le 10^6$).",
    "output_format": "In ra số lượng số nguyên tố $\\le n$.",
    "constraints": "$1 \\le n \\le 10^6$\\nThời gian chạy: 1.5s\\nBộ nhớ: 256MB",
    "sample_input": "10",
    "sample_output": "4",
    "hints": "Sử dụng sàng nguyên tố Eratosthenes để sàng các số nguyên tố tới $n$ một cách nhanh chóng trong $O(n \\log \\log n)$.",
    "python_starter": get_starter_py("Đếm #2"),
    "c_starter": get_starter_c("Đếm #2"),
    "solution_python": """import sys

def solve():
    line = sys.stdin.read().strip()
    if not line:
        return
    n = int(line)
    if n < 2:
        print(0)
        return
    is_prime = bytearray([1]) * (n + 1)
    is_prime[0] = is_prime[1] = 0
    limit = int(n**0.5)
    for i in range(2, limit + 1):
        if is_prime[i]:
            is_prime[i*i : n+1 : i] = bytearray([0]) * len(range(i*i, n+1, i))
    print(sum(is_prime))

if __name__ == '__main__':
    solve()""",
    "solution_c": """#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    int n;
    if (scanf("%d", &n) == 1) {
        if (n < 2) {
            printf("0\\n");
            return 0;
        }
        char *is_prime = (char*)malloc(n + 1);
        memset(is_prime, 1, n + 1);
        is_prime[0] = is_prime[1] = 0;
        for (int i = 2; i * i <= n; i++) {
            if (is_prime[i]) {
                for (int j = i * i; j <= n; j += i) {
                    is_prime[j] = 0;
                }
            }
        }
        int count = 0;
        for (int i = 2; i <= n; i++) {
            if (is_prime[i]) count++;
        }
        printf("%d\\n", count);
        free(is_prime);
    }
    return 0;
}""",
    "editorial": "### Phân Tích & Hướng Dẫn Giải\\n- **Ý tưởng:** Với $n$ lên tới $10^6$, thuật toán sàng nguyên tố Eratosthenes là tối ưu nhất. Khởi tạo mảng boolean đánh dấu từ 0 đến $n$. Lần lượt gạch đi các bội số của các số nguyên tố từ 2 đến $\\sqrt{n}$. Cuối cùng đếm số lượng vị trí còn được đánh dấu.\\n- **Độ phức tạp:** Thời gian $O(n \\log \\log n)$, Bộ nhớ $O(n)$ (khoảng 1MB).",
    "test_cases": [
        {"test_index": 1, "is_sample": True, "description": "Test cơ bản (Mẫu n = 10)", "input_data": "10\n", "expected_output": "4\n"},
        {"test_index": 2, "is_sample": True, "description": "Test không có số nguyên tố (n = 1)", "input_data": "1\n", "expected_output": "0\n"},
        {"test_index": 3, "is_sample": False, "description": "Test số nguyên tố nhỏ nhất (n = 2)", "input_data": "2\n", "expected_output": "1\n"},
        {"test_index": 4, "is_sample": False, "description": "Test n = 100", "input_data": "100\n", "expected_output": "25\n"},
        {"test_index": 5, "is_sample": False, "description": "Stress test n = 10^6", "input_data": "1000000\n", "expected_output": "78498\n"}
    ]
})

# 76: ĐẾM #3
chunk_70_85.append({
    "id": "DRAGON-76",
    "title": "Đếm #3 (Số Chính Phương Trong Dãy)",
    "chapter": "Phần VIII. Mảng một chiều cơ bản",
    "difficulty": "Dễ",
    "time_limit": 1.5,
    "memory_limit": 256,
    "description": "Nhập vào dãy số $A$ có $n$ phần tử. Đếm xem trong dãy $A$ có bao nhiêu số là số chính phương.",
    "input_format": "Dòng 1: Số nguyên dương $n$ ($1 \\le n \\le 100$).\\nDòng 2: $n$ số nguyên dương $a_i$ ($1 \\le a_i \\le 10^6$), cách nhau bởi khoảng trắng.",
    "output_format": "In ra số lượng số chính phương có trong dãy $A$.",
    "constraints": "$1 \\le n \\le 100$\\n$1 \\le a_i \\le 10^6$\\nThời gian chạy: 1.5s\\nBộ nhớ: 256MB",
    "sample_input": "5\n1 2 3 4 5",
    "sample_output": "2",
    "hints": "Kiểm tra từng phần tử $x$: tính $k = \\lfloor\\sqrt{x}\\rfloor$, nếu $k \\times k == x$ thì $x$ là số chính phương.",
    "python_starter": get_starter_py("Đếm #3"),
    "c_starter": get_starter_c("Đếm #3"),
    "solution_python": """import sys
import math

def solve():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    nums = [int(x) for x in tokens[1:n+1]]
    count = 0
    for x in nums:
        if x >= 0:
            k = math.isqrt(x)
            if k * k == x:
                count += 1
    print(count)

if __name__ == '__main__':
    solve()""",
    "solution_c": """#include <stdio.h>
#include <math.h>

int main() {
    int n;
    if (scanf("%d", &n) == 1) {
        int count = 0;
        for (int i = 0; i < n; i++) {
            long long x;
            if (scanf("%lld", &x) == 1) {
                if (x >= 0) {
                    long long k = (long long)sqrt(x);
                    if (k * k == x) count++;
                }
            }
        }
        printf("%d\\n", count);
    }
    return 0;
}""",
    "editorial": "### Phân Tích & Hướng Dẫn Giải\\n- **Ý tưởng:** Duyệt qua từng số $a_i$ trong mảng, kiểm tra xem $a_i$ có thỏa mãn $(\\lfloor\\sqrt{a_i}\\rfloor)^2 == a_i$ hay không. Nếu có thì tăng biến đếm.\\n- **Độ phức tạp:** Thời gian $O(n)$, Bộ nhớ $O(1)$.",
    "test_cases": [
        {"test_index": 1, "is_sample": True, "description": "Test cơ bản (Mẫu)", "input_data": "5\n1 2 3 4 5\n", "expected_output": "2\n"},
        {"test_index": 2, "is_sample": True, "description": "Toàn bộ là chính phương", "input_data": "4\n9 16 25 36\n", "expected_output": "4\n"},
        {"test_index": 3, "is_sample": False, "description": "Không có số chính phương nào", "input_data": "3\n2 3 5\n", "expected_output": "0\n"},
        {"test_index": 4, "is_sample": False, "description": "Mảng 1 phần tử lớn 10^6", "input_data": "1\n1000000\n", "expected_output": "1\n"},
        {"test_index": 5, "is_sample": False, "description": "Hỗn hợp nhiều số", "input_data": "8\n10 16 20 25 30 49 64 80\n", "expected_output": "4\n"}
    ]
})

# 77: ĐẾM #4
chunk_70_85.append({
    "id": "DRAGON-77",
    "title": "Đếm #4 (Số Nguyên Tố Trong Dãy)",
    "chapter": "Phần VIII. Mảng một chiều cơ bản",
    "difficulty": "Dễ",
    "time_limit": 1.5,
    "memory_limit": 256,
    "description": "Nhập vào dãy $A$ có $n$ phần tử. Đếm xem trong dãy $A$ có bao nhiêu số là số nguyên tố.",
    "input_format": "Dòng 1: Số nguyên dương $n$ ($1 \\le n \\le 1000$).\\nDòng 2: $n$ số nguyên dương $a_i$ ($1 \\le a_i \\le 10^6$), cách nhau bởi khoảng trắng.",
    "output_format": "In ra số lượng số nguyên tố có trong dãy $A$.",
    "constraints": "$1 \\le n \\le 1000$\\n$1 \\le a_i \\le 10^6$\\nThời gian chạy: 1.5s\\nBộ nhớ: 256MB",
    "sample_input": "5\n1 2 3 4 5",
    "sample_output": "3",
    "hints": "Viết một hàm kiểm tra số nguyên tố $O(\\sqrt{x})$, duyệt qua từng phần tử của dãy và đếm.",
    "python_starter": get_starter_py("Đếm #4"),
    "c_starter": get_starter_c("Đếm #4"),
    "solution_python": """import sys
import math

def is_prime(x):
    if x < 2:
        return False
    if x in (2, 3):
        return True
    if x % 2 == 0 or x % 3 == 0:
        return False
    i = 5
    while i * i <= x:
        if x % i == 0 or x % (i + 2) == 0:
            return False
        i += 6
    return True

def solve():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    nums = [int(x) for x in tokens[1:n+1]]
    count = sum(1 for x in nums if is_prime(x))
    print(count)

if __name__ == '__main__':
    solve()""",
    "solution_c": """#include <stdio.h>
#include <stdbool.h>

bool is_prime(long long x) {
    if (x < 2) return false;
    if (x == 2 || x == 3) return true;
    if (x % 2 == 0 || x % 3 == 0) return false;
    for (long long i = 5; i * i <= x; i += 6) {
        if (x % i == 0 || x % (i + 2) == 0) return false;
    }
    return true;
}

int main() {
    int n;
    if (scanf("%d", &n) == 1) {
        int count = 0;
        for (int i = 0; i < n; i++) {
            long long x;
            if (scanf("%lld", &x) == 1) {
                if (is_prime(x)) count++;
            }
        }
        printf("%d\\n", count);
    }
    return 0;
}""",
    "editorial": "### Phân Tích & Hướng Dẫn Giải\\n- **Ý tưởng:** Với mỗi số $a_i \\le 10^6$, ta kiểm tra tính nguyên tố bằng cách duyệt các ước tới $\\sqrt{a_i}$. Vì $n \\le 1000$ và $\\sqrt{a_i} \\le 1000$, tổng số phép tính tối đa là $1000 \\times 1000 / 6 \\approx 1.6 \\times 10^5$, thực thi trong chưa đầy 5ms.\\n- **Độ phức tạp:** Thời gian $O(n \\sqrt{\\max A})$, Bộ nhớ $O(1)$.",
    "test_cases": [
        {"test_index": 1, "is_sample": True, "description": "Test cơ bản (Mẫu)", "input_data": "5\n1 2 3 4 5\n", "expected_output": "3\n"},
        {"test_index": 2, "is_sample": True, "description": "Không có số nguyên tố nào", "input_data": "4\n1 4 6 8\n", "expected_output": "0\n"},
        {"test_index": 3, "is_sample": False, "description": "Toàn bộ là số nguyên tố", "input_data": "3\n13 17 19\n", "expected_output": "3\n"},
        {"test_index": 4, "is_sample": False, "description": "Số 2 là nguyên tố chẵn duy nhất", "input_data": "1\n2\n", "expected_output": "1\n"},
        {"test_index": 5, "is_sample": False, "description": "Dãy nhiều số nguyên tố lớn", "input_data": "7\n11 23 29 31 37 41 43\n", "expected_output": "7\n"}
    ]
})

# 78: ĐẾM #5
chunk_70_85.append({
    "id": "DRAGON-78",
    "title": "Đếm #5 (Số May Mắn Trong Dãy)",
    "chapter": "Phần VIII. Mảng một chiều cơ bản",
    "difficulty": "Dễ",
    "time_limit": 1.5,
    "memory_limit": 256,
    "description": "Nhập vào dãy $A$ có $n$ phần tử. Đếm xem trong dãy $A$ có bao nhiêu số là số may mắn (số may mắn là số nguyên dương chia hết cho tổng các chữ số của nó).",
    "input_format": "Dòng 1: Số nguyên dương $n$ ($1 \\le n \\le 1000$).\\nDòng 2: $n$ số nguyên dương $a_i$ ($1 \\le a_i \\le 10^6$), cách nhau bởi khoảng trắng.",
    "output_format": "In ra số lượng số may mắn trong dãy.",
    "constraints": "$1 \\le n \\le 1000$\\n$1 \\le a_i \\le 10^6$\\nThời gian chạy: 1.5s\\nBộ nhớ: 256MB",
    "sample_input": "5\n1 12 3 14 5",
    "sample_output": "4",
    "hints": "Với mỗi phần tử $x$, tính tổng các chữ số của $x$, sau đó kiểm tra xem $x \\% (\\text{tổng chữ số}) == 0$.",
    "python_starter": get_starter_py("Đếm #5"),
    "c_starter": get_starter_c("Đếm #5"),
    "solution_python": """import sys

def is_lucky(x):
    if x <= 0:
        return False
    temp = x
    s = 0
    while temp > 0:
        s += temp % 10
        temp //= 10
    return s > 0 and (x % s == 0)

def solve():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    nums = [int(x) for x in tokens[1:n+1]]
    count = sum(1 for x in nums if is_lucky(x))
    print(count)

if __name__ == '__main__':
    solve()""",
    "solution_c": """#include <stdio.h>
#include <stdbool.h>

bool is_lucky(long long x) {
    if (x <= 0) return false;
    long long temp = x;
    long long s = 0;
    while (temp > 0) {
        s += temp % 10;
        temp /= 10;
    }
    return (s > 0 && x % s == 0);
}

int main() {
    int n;
    if (scanf("%d", &n) == 1) {
        int count = 0;
        for (int i = 0; i < n; i++) {
            long long x;
            if (scanf("%lld", &x) == 1) {
                if (is_lucky(x)) count++;
            }
        }
        printf("%d\\n", count);
    }
    return 0;
}""",
    "editorial": "### Phân Tích & Hướng Dẫn Giải\\n- **Ý tưởng:** Với mỗi phần tử $x$ trong dãy, ta tách từng chữ số của $x$ để tính tổng $S$. Nếu $x \\% S == 0$ thì $x$ là số Harshad (số may mắn), ta tăng biến đếm.\\n- **Độ phức tạp:** Thời gian $O(n \\log_{10}(\\max A))$, Bộ nhớ $O(1)$.",
    "test_cases": [
        {"test_index": 1, "is_sample": True, "description": "Test cơ bản (Mẫu)", "input_data": "5\n1 12 3 14 5\n", "expected_output": "4\n"},
        {"test_index": 2, "is_sample": True, "description": "Toàn bộ là số may mắn", "input_data": "3\n10 18 20\n", "expected_output": "3\n"},
        {"test_index": 3, "is_sample": False, "description": "Không có số may mắn nào", "input_data": "3\n11 13 17\n", "expected_output": "0\n"},
        {"test_index": 4, "is_sample": False, "description": "Số tròn trăm", "input_data": "1\n100\n", "expected_output": "1\n"},
        {"test_index": 5, "is_sample": False, "description": "Nhiều số bội số của tổng chữ số", "input_data": "6\n21 24 27 30 36 42\n", "expected_output": "6\n"}
    ]
})

# 79: TỔNG ƯỚC
chunk_70_85.append({
    "id": "DRAGON-79",
    "title": "Tổng Ước Của Một Số",
    "chapter": "Phần V. Bài toán phân tích & Số học",
    "difficulty": "Trung bình",
    "time_limit": 1.5,
    "memory_limit": 256,
    "description": "Nhập vào một số nguyên dương $n$. Hãy tính và in ra tổng tất cả các ước số nguyên dương của $n$.",
    "input_format": "Một dòng duy nhất chứa số nguyên dương $n$ ($1 \\le n \\le 10^6$).",
    "output_format": "In ra một số nguyên duy nhất là tổng tất cả các ước của $n$.",
    "constraints": "$1 \\le n \\le 10^6$\\nThời gian chạy: 1.5s\\nBộ nhớ: 256MB",
    "sample_input": "6",
    "sample_output": "12",
    "hints": "Duyệt $i$ từ 1 đến $\\sqrt{n}$. Nếu $n \\% i == 0$, cộng $i$ và cả ước đối xứng $n / i$ (chú ý trường hợp $i == n / i$).",
    "python_starter": get_starter_py("Tổng Ước"),
    "c_starter": get_starter_c("Tổng Ước"),
    "solution_python": """import sys
import math

def solve():
    line = sys.stdin.read().strip()
    if not line:
        return
    n = int(line)
    total = 0
    limit = math.isqrt(n)
    for i in range(1, limit + 1):
        if n % i == 0:
            total += i
            if i * i != n:
                total += n // i
    print(total)

if __name__ == '__main__':
    solve()""",
    "solution_c": """#include <stdio.h>
#include <math.h>

int main() {
    long long n;
    if (scanf("%lld", &n) == 1) {
        long long total = 0;
        long long limit = (long long)sqrt(n);
        for (long long i = 1; i <= limit; i++) {
            if (n % i == 0) {
                total += i;
                if (i * i != n) {
                    total += n / i;
                }
            }
        }
        printf("%lld\\n", total);
    }
    return 0;
}""",
    "editorial": "### Phân Tích & Hướng Dẫn Giải\\n- **Ý tưởng:** Nếu $i$ là ước của $n$ thì $n/i$ cũng là ước của $n$. Do đó ta chỉ cần duyệt $i$ từ $1$ đến $\\sqrt{n}$. Khi tìm thấy $n \\% i == 0$, cộng cả $i$ và $n/i$ vào tổng (nếu $i = \\sqrt{n}$ thì chỉ cộng 1 lần).\\n- **Độ phức tạp:** Thời gian $O(\\sqrt{n})$, Bộ nhớ $O(1)$.",
    "test_cases": [
        {"test_index": 1, "is_sample": True, "description": "Test cơ bản (Mẫu n = 6)", "input_data": "6\n", "expected_output": "12\n"},
        {"test_index": 2, "is_sample": True, "description": "Test n = 1", "input_data": "1\n", "expected_output": "1\n"},
        {"test_index": 3, "is_sample": False, "description": "Số hoàn hảo 28", "input_data": "28\n", "expected_output": "56\n"},
        {"test_index": 4, "is_sample": False, "description": "Số nguyên tố 13", "input_data": "13\n", "expected_output": "14\n"},
        {"test_index": 5, "is_sample": False, "description": "Biên trên n = 10^6", "input_data": "1000000\n", "expected_output": "2480437\n"}
    ]
})

# 80, 81 from existing
chunk_70_85.append(existing_dict["DRAGON-80"])
chunk_70_85.append(existing_dict["DRAGON-81"])

# 82: TÍCH LẤY DƯ
chunk_70_85.append({
    "id": "DRAGON-82",
    "title": "Tích Lấy Dư Trong Đoạn [a, b]",
    "chapter": "Phần V. Bài toán phân tích & Số học",
    "difficulty": "Trung bình",
    "time_limit": 1.5,
    "memory_limit": 256,
    "description": "Nhập vào 3 số nguyên dương $a, b, c$. In ra số dư của phép chia tích các số nguyên trong đoạn $[a, b]$ cho $c$ (tức $(a \\times (a+1) \\times \\dots \\times b) \\pmod c$).",
    "input_format": "Một dòng chứa ba số nguyên dương $a, b, c$ ($1 \\le a \\le b \\le 10^5, 1 \\le c \\le 10^9$), cách nhau bởi khoảng trắng.",
    "output_format": "In ra số dư tìm được.",
    "constraints": "$1 \\le a \\le b \\le 10^5$\\n$1 \\le c \\le 10^9$\\nThời gian chạy: 1.5s\\nBộ nhớ: 256MB",
    "sample_input": "5 10 11",
    "sample_output": "5",
    "hints": "Nhân dồn từ $a$ đến $b$ và lấy modulo $c$ sau mỗi bước: `ans = (ans * i) % c`. Nếu `ans == 0` thì có thể dừng sớm.",
    "python_starter": get_starter_py("Tích Lấy Dư"),
    "c_starter": get_starter_c("Tích Lấy Dư"),
    "solution_python": """import sys

def solve():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    a, b, c = int(tokens[0]), int(tokens[1]), int(tokens[2])
    ans = 1
    for i in range(a, b + 1):
        ans = (ans * (i % c)) % c
        if ans == 0:
            break
    print(ans)

if __name__ == '__main__':
    solve()""",
    "solution_c": """#include <stdio.h>

int main() {
    long long a, b, c;
    if (scanf("%lld %lld %lld", &a, &b, &c) == 3) {
        long long ans = 1;
        for (long long i = a; i <= b; i++) {
            ans = (ans * (i % c)) % c;
            if (ans == 0) break;
        }
        printf("%lld\\n", ans);
    }
    return 0;
}""",
    "editorial": "### Phân Tích & Hướng Dẫn Giải\\n- **Ý tưởng:** Áp dụng tính chất phân phối của phép nhân modulo: $(x \\times y) \\pmod c = ((x \\pmod c) \\times (y \\pmod c)) \\pmod c$. Vòng lặp chạy từ $a$ đến $b$. Nếu tại bất kỳ bước nào kết quả trung gian bằng 0 (chia hết cho $c$), ta có thể ngắt sớm để tiết kiệm thời gian.\\n- **Độ phức tạp:** Thời gian $O(b - a + 1) \\le 10^5$, Bộ nhớ $O(1)$.",
    "test_cases": [
        {"test_index": 1, "is_sample": True, "description": "Test cơ bản (Mẫu 5..10 % 11)", "input_data": "5 10 11\n", "expected_output": "5\n"},
        {"test_index": 2, "is_sample": True, "description": "Đoạn nhỏ 1..5 % 7", "input_data": "1 5 7\n", "expected_output": "1\n"},
        {"test_index": 3, "is_sample": False, "description": "a == b", "input_data": "10 10 13\n", "expected_output": "10\n"},
        {"test_index": 4, "is_sample": False, "description": "Đoạn chứa c nên chia hết (mod = 0)", "input_data": "1 100 97\n", "expected_output": "0\n"},
        {"test_index": 5, "is_sample": False, "description": "Đoạn lớn 1000..2000 modulo 10^9+7", "input_data": "1000 2000 1000000007\n", "expected_output": "649176378\n"}
    ]
})

# 83: TRỌNG SỐ
chunk_70_85.append({
    "id": "DRAGON-83",
    "title": "Trọng Số Của Dãy Số",
    "chapter": "Phần VIII. Mảng một chiều cơ bản",
    "difficulty": "Dễ",
    "time_limit": 1.5,
    "memory_limit": 256,
    "description": "Cho dãy số nguyên dương $A = (a_1, a_2, \\dots, a_n)$. Trọng số của dãy $A$ được tính theo công thức: $C = 1 \\times a_1 + 2 \\times a_2 + \\dots + n \\times a_n$. Hãy tính và in ra giá trị $C$.",
    "input_format": "Dòng 1: Số nguyên dương $n$ ($1 \\le n \\le 1000$).\\nDòng 2: $n$ số nguyên dương $a_i$ ($1 \\le a_i \\le 10^6$), cách nhau bởi khoảng trắng.",
    "output_format": "In ra một số nguyên là trọng số của dãy $A$.",
    "constraints": "$1 \\le n \\le 1000$\\n$1 \\le a_i \\le 10^6$\\nThời gian chạy: 1.5s\\nBộ nhớ: 256MB",
    "sample_input": "4\n4 3 2 5",
    "sample_output": "36",
    "hints": "Sử dụng kiểu dữ liệu `long long` trong C để tránh tràn số vì tổng trọng số có thể đạt tới $1000 \\times 1000 \\times 10^6 / 2 \\approx 5 \\times 10^{11}$.",
    "python_starter": get_starter_py("Trọng Số"),
    "c_starter": get_starter_c("Trọng Số"),
    "solution_python": """import sys

def solve():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    nums = [int(x) for x in tokens[1:n+1]]
    total = sum((i + 1) * nums[i] for i in range(n))
    print(total)

if __name__ == '__main__':
    solve()""",
    "solution_c": """#include <stdio.h>

int main() {
    int n;
    if (scanf("%d", &n) == 1) {
        long long total = 0;
        for (int i = 1; i <= n; i++) {
            long long a;
            if (scanf("%lld", &a) == 1) {
                total += (long long)i * a;
            }
        }
        printf("%lld\\n", total);
    }
    return 0;
}""",
    "editorial": "### Phân Tích & Hướng Dẫn Giải\\n- **Ý tưởng:** Duyệt vòng lặp từ $i = 1$ đến $n$, nhân chỉ số $i$ với phần tử $a_i$ và cộng dồn vào biến `total`. Chú ý dùng kiểu `long long` trong C vì kết quả có thể vượt quá $2 \\times 10^9$.\\n- **Độ phức tạp:** Thời gian $O(n)$, Bộ nhớ $O(1)$.",
    "test_cases": [
        {"test_index": 1, "is_sample": True, "description": "Test cơ bản (Mẫu)", "input_data": "4\n4 3 2 5\n", "expected_output": "36\n"},
        {"test_index": 2, "is_sample": True, "description": "Mảng 1 phần tử", "input_data": "1\n100\n", "expected_output": "100\n"},
        {"test_index": 3, "is_sample": False, "description": "Toàn bộ là 1 (Tổng dãy tự nhiên)", "input_data": "5\n1 1 1 1 1\n", "expected_output": "15\n"},
        {"test_index": 4, "is_sample": False, "description": "Mảng tăng dần", "input_data": "3\n10 20 30\n", "expected_output": "140\n"},
        {"test_index": 5, "is_sample": False, "description": "Mảng nhiều phần tử", "input_data": "6\n500 1000 1500 2000 2500 3000\n", "expected_output": "42000\n"}
    ]
})

# 84 from existing
chunk_70_85.append(existing_dict["DRAGON-84"])

# 85: CHUYỂN SỐ 2
chunk_70_85.append({
    "id": "DRAGON-85",
    "title": "Chuyển Số 2 (Nhị Phân Sang Thập Phân)",
    "chapter": "Phần VII. Xử lý chữ số",
    "difficulty": "Dễ",
    "time_limit": 1.5,
    "memory_limit": 256,
    "description": "Nhập vào số $n$ ở hệ nhị phân (gồm các ký tự '0' và '1'). Hãy chuyển số $n$ sang hệ thập phân và in ra màn hình.",
    "input_format": "Một dòng duy nhất chứa chuỗi ký tự nhị phân $n$ (độ dài chuỗi $\\le 60$).",
    "output_format": "In ra giá trị của số đó ở hệ thập phân.",
    "constraints": "Độ dài chuỗi nhị phân $\\le 60$\\nThời gian chạy: 1.5s\\nBộ nhớ: 256MB",
    "sample_input": "101",
    "sample_output": "5",
    "hints": "Duyệt từng ký tự từ trái qua phải: `ans = ans * 2 + (ch - '0')`.",
    "python_starter": get_starter_py("Chuyển Số 2"),
    "c_starter": get_starter_c("Chuyển Số 2"),
    "solution_python": """import sys

def solve():
    line = sys.stdin.read().strip()
    if not line:
        return
    print(int(line, 2))

if __name__ == '__main__':
    solve()""",
    "solution_c": """#include <stdio.h>
#include <string.h>

int main() {
    char s[100];
    if (scanf("%s", s) == 1) {
        unsigned long long ans = 0;
        for (int i = 0; s[i] != '\\0'; i++) {
            ans = ans * 2 + (s[i] - '0');
        }
        printf("%llu\\n", ans);
    }
    return 0;
}""",
    "editorial": "### Phân Tích & Hướng Dẫn Giải\\n- **Ý tưởng:** Đọc xâu nhị phân. Duyệt từ đầu đến cuối xâu, mỗi bước nhân giá trị tích lũy với 2 rồi cộng thêm giá trị chữ số hiện tại ($0$ hoặc $1$). Vì độ dài chuỗi $\\le 60$, kết quả chứa vừa vặn trong kiểu `unsigned long long` 64-bit trong C (tối đa tới $2^{64}-1$).\\n- **Độ phức tạp:** Thời gian $O(L)$ với $L$ là độ dài chuỗi, Bộ nhớ $O(1)$.",
    "test_cases": [
        {"test_index": 1, "is_sample": True, "description": "Test cơ bản (Mẫu 101)", "input_data": "101\n", "expected_output": "5\n"},
        {"test_index": 2, "is_sample": True, "description": "Test số 0", "input_data": "0\n", "expected_output": "0\n"},
        {"test_index": 3, "is_sample": False, "description": "Test 1111 (15)", "input_data": "1111\n", "expected_output": "15\n"},
        {"test_index": 4, "is_sample": False, "description": "Lũy thừa của 2 (256)", "input_data": "100000000\n", "expected_output": "256\n"},
        {"test_index": 5, "is_sample": False, "description": "Chuỗi dài (30 chữ số 1)", "input_data": "111111111111111111111111111111\n", "expected_output": "1073741823\n"}
    ]
})

with open('data_generators/problems_70_85.py', 'w', encoding='utf-8') as f:
    f.write('problems = ' + repr(chunk_70_85) + '\n')

print(f"Generated data_generators/problems_70_85.py with {len(chunk_70_85)} problems!")
