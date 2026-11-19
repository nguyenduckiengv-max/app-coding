# Generator for problems DRAGON-86 through DRAGON-100
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

chunk_86_100 = []

# 86: CHIA BĂNG SỐ
chunk_86_100.append({
    "id": "DRAGON-86",
    "title": "Chia Băng Số (Đoạn Bằng Nhau)",
    "chapter": "Phần VIII. Mảng một chiều cơ bản",
    "difficulty": "Trung bình",
    "time_limit": 1.5,
    "memory_limit": 256,
    "description": "Nhập vào 1 băng số có $n$ phần tử nguyên dương $a_1, a_2, \\dots, a_n$. Hãy chia băng số này thành nhiều đoạn con liên tiếp nhất sao cho tổng các phần tử trong mỗi đoạn bằng nhau. In ra số đoạn nhiều nhất có thể chia được.",
    "input_format": "Dòng 1: Số nguyên dương $n$ ($1 \\le n \\le 1000$).\\nDòng 2: $n$ số nguyên dương $a_i$ ($1 \\le a_i \\le 1000$), cách nhau bởi khoảng trắng.",
    "output_format": "In ra số đoạn nhiều nhất có thể chia được.",
    "constraints": "$1 \\le n \\le 1000$\\n$1 \\le a_i \\le 1000$\\nThời gian chạy: 1.5s\\nBộ nhớ: 256MB",
    "sample_input": "8\n10 2 6 2 5 2 1 2",
    "sample_output": "3",
    "hints": "Tổng mảng là $S$. Thử số đoạn $k$ từ $n$ giảm dần về 1. Nếu $S \\% k == 0$, kiểm tra xem có thể cộng dồn tạo thành $k$ đoạn tổng $S/k$ không.",
    "python_starter": get_starter_py("Chia Băng Số"),
    "c_starter": get_starter_c("Chia Băng Số"),
    "solution_python": """import sys

def solve():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    nums = [int(x) for x in tokens[1:n+1]]
    total = sum(nums)
    for k in range(n, 1, -1):
        if total % k == 0:
            target = total // k
            cur = 0
            possible = True
            for x in nums:
                cur += x
                if cur == target:
                    cur = 0
                elif cur > target:
                    possible = False
                    break
            if possible and cur == 0:
                print(k)
                return
    print(1)

if __name__ == '__main__':
    solve()""",
    "solution_c": """#include <stdio.h>
#include <stdbool.h>

int main() {
    int n;
    if (scanf("%d", &n) == 1) {
        long long a[1005];
        long long total = 0;
        for (int i = 0; i < n; i++) {
            scanf("%lld", &a[i]);
            total += a[i];
        }
        for (int k = n; k >= 2; k--) {
            if (total % k == 0) {
                long long target = total / k;
                long long cur = 0;
                bool ok = true;
                for (int i = 0; i < n; i++) {
                    cur += a[i];
                    if (cur == target) {
                        cur = 0;
                    } else if (cur > target) {
                        ok = false;
                        break;
                    }
                }
                if (ok && cur == 0) {
                    printf("%d\\n", k);
                    return 0;
                }
            }
        }
        printf("1\\n");
    }
    return 0;
}""",
    "editorial": "### Phân Tích & Hướng Dẫn Giải\\n- **Ý tưởng:** Giả sử ta chia mảng thành $k$ đoạn có tổng bằng nhau thì tổng toàn mảng $S$ phải chia hết cho $k$, và tổng mỗi đoạn là $T = S / k$. Vì cần tìm $k$ lớn nhất, ta thử $k$ giảm dần từ $n$ về 1. Với mỗi $k$, ta duyệt mảng và cộng dồn các phần tử; khi tổng đạt đúng $T$ ta bắt đầu đoạn mới. Nếu gặp tổng con vượt quá $T$ thì cách chia không hợp lệ.\\n- **Độ phức tạp:** Thời gian $O(n \\cdot d(S))$ với $d(S)$ là số ước số của $S$, Bộ nhớ $O(n)$.",
    "test_cases": [
        {"test_index": 1, "is_sample": True, "description": "Test cơ bản (Mẫu 1: 3 đoạn tổng 10)", "input_data": "8\n10 2 6 2 5 2 1 2\n", "expected_output": "3\n"},
        {"test_index": 2, "is_sample": True, "description": "Không thể chia (Mẫu 2: 1 đoạn)", "input_data": "5\n1 2 3 4 5\n", "expected_output": "1\n"},
        {"test_index": 3, "is_sample": False, "description": "Mọi phần tử bằng nhau (chia k = n)", "input_data": "4\n5 5 5 5\n", "expected_output": "4\n"},
        {"test_index": 4, "is_sample": False, "description": "Chia làm 2 nửa đối xứng", "input_data": "6\n1 2 3 3 2 1\n", "expected_output": "2\n"},
        {"test_index": 5, "is_sample": False, "description": "Mảng toàn số 2", "input_data": "6\n2 2 2 2 2 2\n", "expected_output": "6\n"}
    ]
})

# 87: XÂU FIBONACCI
chunk_86_100.append({
    "id": "DRAGON-87",
    "title": "Xâu Fibonacci",
    "chapter": "Phần VI. Dãy số & Đệ quy cơ bản",
    "difficulty": "Dễ",
    "time_limit": 1.5,
    "memory_limit": 256,
    "description": "Nhập vào 1 số nguyên dương $n$. In ra xâu Fibonacci thứ $n$.\\nĐịnh nghĩa xâu Fibonacci:\\n- $f(1) = \\text{'A'}$\\n- $f(2) = \\text{'B'}$\\n- $f(i) = f(i-1) + f(i-2)$ với mọi $i \\ge 3$ (phép $+$ là phép ghép hai xâu).",
    "input_format": "Một dòng duy nhất chứa số nguyên dương $n$ ($1 \\le n \\le 20$).",
    "output_format": "In ra xâu Fibonacci thứ $n$.",
    "constraints": "$1 \\le n \\le 20$\\nThời gian chạy: 1.5s\\nBộ nhớ: 256MB",
    "sample_input": "3",
    "sample_output": "BA",
    "hints": "Với $n \\le 20$, độ dài xâu Fibonacci tối đa chỉ vài nghìn ký tự. Ta có thể nối chuỗi trực tiếp từ $f(1)$ và $f(2)$.",
    "python_starter": get_starter_py("Xâu Fibonacci"),
    "c_starter": get_starter_c("Xâu Fibonacci"),
    "solution_python": """import sys

def solve():
    line = sys.stdin.read().strip()
    if not line:
        return
    n = int(line)
    if n == 1:
        print("A")
        return
    if n == 2:
        print("B")
        return
    f1 = "A"
    f2 = "B"
    for _ in range(3, n + 1):
        f_next = f2 + f1
        f1 = f2
        f2 = f_next
    print(f2)

if __name__ == '__main__':
    solve()""",
    "solution_c": """#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main() {
    int n;
    if (scanf("%d", &n) == 1) {
        if (n == 1) {
            printf("A\\n");
            return 0;
        }
        if (n == 2) {
            printf("B\\n");
            return 0;
        }
        char *f1 = (char*)malloc(1000000);
        char *f2 = (char*)malloc(1000000);
        char *f3 = (char*)malloc(1000000);
        strcpy(f1, "A");
        strcpy(f2, "B");
        for (int i = 3; i <= n; i++) {
            strcpy(f3, f2);
            strcat(f3, f1);
            strcpy(f1, f2);
            strcpy(f2, f3);
        }
        printf("%s\\n", f2);
        free(f1); free(f2); free(f3);
    }
    return 0;
}""",
    "editorial": "### Phân Tích & Hướng Dẫn Giải\\n- **Ý tưởng:** Bắt đầu với $f(1) = \\text{\"A\"}$ và $f(2) = \\text{\"B\"}$. Ở mỗi bước thứ $i \\ge 3$, xâu mới được tạo bằng cách nối $f(i-1)$ với $f(i-2)$ (chú ý thứ tự là $f(i-1) + f(i-2)$). Với $n \\le 20$, xâu $f(20)$ có độ dài $6765$ ký tự, hoàn toàn vừa trong bộ nhớ và chạy tức thời.\\n- **Độ phức tạp:** Thời gian $O(\\text{len}(f(n)))$, Bộ nhớ $O(\\text{len}(f(n)))$.",
    "test_cases": [
        {"test_index": 1, "is_sample": True, "description": "Test cơ bản (Mẫu 1 n = 3)", "input_data": "3\n", "expected_output": "BA\n"},
        {"test_index": 2, "is_sample": True, "description": "Test mẫu 2 (n = 6)", "input_data": "6\n", "expected_output": "BABBABAB\n"},
        {"test_index": 3, "is_sample": False, "description": "Biên dưới (n = 1)", "input_data": "1\n", "expected_output": "A\n"},
        {"test_index": 4, "is_sample": False, "description": "Biên dưới (n = 2)", "input_data": "2\n", "expected_output": "B\n"},
        {"test_index": 5, "is_sample": False, "description": "Xâu n = 7", "input_data": "7\n", "expected_output": "BABBABABBABBA\n"}
    ]
})

# 88 from existing
chunk_86_100.append(existing_dict["DRAGON-88"])

# 89: ĐOẠN CON #2
chunk_86_100.append({
    "id": "DRAGON-89",
    "title": "Đoạn Con #2 (Phần Tử Dương Dài Nhất)",
    "chapter": "Phần VIII. Mảng một chiều cơ bản",
    "difficulty": "Dễ",
    "time_limit": 1.5,
    "memory_limit": 256,
    "description": "Nhập vào mảng $A$ gồm $n$ phần tử. Tìm độ dài của đoạn con liên tiếp dài nhất chỉ chứa các phần tử dương ($a_i > 0$).",
    "input_format": "Dòng 1: Số nguyên dương $n$ ($1 \\le n \\le 1000$).\\nDòng 2: $n$ số nguyên $a_i$ ($-10^6 \\le a_i \\le 10^6$), cách nhau bởi khoảng trắng.",
    "output_format": "In ra số lượng phần tử của đoạn con tìm được.",
    "constraints": "$1 \\le n \\le 1000$\\n$-10^6 \\le a_i \\le 10^6$\\nThời gian chạy: 1.5s\\nBộ nhớ: 256MB",
    "sample_input": "8\n1 2 2 -2 3 -4 3 3",
    "sample_output": "3",
    "hints": "Duyệt qua mảng: nếu phần tử $> 0$, tăng biến đếm đoạn hiện tại; ngược lại reset về 0. Luôn cập nhật độ dài lớn nhất.",
    "python_starter": get_starter_py("Đoạn Con #2"),
    "c_starter": get_starter_c("Đoạn Con #2"),
    "solution_python": """import sys

def solve():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    nums = [int(x) for x in tokens[1:n+1]]
    max_len = 0
    cur_len = 0
    for x in nums:
        if x > 0:
            cur_len += 1
            if cur_len > max_len:
                max_len = cur_len
        else:
            cur_len = 0
    print(max_len)

if __name__ == '__main__':
    solve()""",
    "solution_c": """#include <stdio.h>

int main() {
    int n;
    if (scanf("%d", &n) == 1) {
        int max_len = 0, cur_len = 0;
        for (int i = 0; i < n; i++) {
            long long x;
            if (scanf("%lld", &x) == 1) {
                if (x > 0) {
                    cur_len++;
                    if (cur_len > max_len) max_len = cur_len;
                } else {
                    cur_len = 0;
                }
            }
        }
        printf("%d\\n", max_len);
    }
    return 0;
}""",
    "editorial": "### Phân Tích & Hướng Dẫn Giải\\n- **Ý tưởng:** Duyệt tuyến tính qua mảng với biến đếm `cur_len`. Nếu gặp số dương ($x > 0$), tăng `cur_len` và cập nhật `max_len = max(max_len, cur_len)`. Nếu gặp số không dương ($x \\le 0$), đặt lại `cur_len = 0`.\\n- **Độ phức tạp:** Thời gian $O(n)$, Bộ nhớ $O(1)$.",
    "test_cases": [
        {"test_index": 1, "is_sample": True, "description": "Test cơ bản (Mẫu)", "input_data": "8\n1 2 2 -2 3 -4 3 3\n", "expected_output": "3\n"},
        {"test_index": 2, "is_sample": True, "description": "Toàn bộ là số âm", "input_data": "5\n-1 -2 -3 -4 -5\n", "expected_output": "0\n"},
        {"test_index": 3, "is_sample": False, "description": "Toàn bộ là số dương", "input_data": "5\n1 2 3 4 5\n", "expected_output": "5\n"},
        {"test_index": 4, "is_sample": False, "description": "Có số 0 ngắt đoạn", "input_data": "6\n2 0 3 4 5 0\n", "expected_output": "3\n"},
        {"test_index": 5, "is_sample": False, "description": "Đoạn dương ở giữa mảng", "input_data": "10\n1 2 -1 3 4 5 6 -2 7 8\n", "expected_output": "4\n"}
    ]
})

# 90: ĐOẠN CON #3
chunk_86_100.append({
    "id": "DRAGON-90",
    "title": "Đoạn Con #3 (Đơn Điệu Dài Nhất)",
    "chapter": "Phần VIII. Mảng một chiều cơ bản",
    "difficulty": "Trung bình",
    "time_limit": 1.5,
    "memory_limit": 256,
    "description": "Nhập vào mảng $A$ gồm $n$ phần tử. Tìm độ dài đoạn con liên tiếp dài nhất chứa các phần tử tăng dần hoặc giảm dần (tăng nghiêm ngặt hoặc giảm nghiêm ngặt: $a_i < a_{i+1}$ hoặc $a_i > a_{i+1}$).",
    "input_format": "Dòng 1: Số nguyên dương $n$ ($1 \\le n \\le 1000$).\\nDòng 2: $n$ số nguyên $a_i$ ($-10^6 \\le a_i \\le 10^6$), cách nhau bởi khoảng trắng.",
    "output_format": "In ra độ dài lớn nhất của đoạn con tìm được.",
    "constraints": "$1 \\le n \\le 1000$\\n$-10^6 \\le a_i \\le 10^6$\\nThời gian chạy: 1.5s\\nBộ nhớ: 256MB",
    "sample_input": "8\n1 2 2 -2 -2 2 3 5",
    "sample_output": "4",
    "hints": "Duy trì hai biến độ dài: `inc` (đang tăng) và `dec` (đang giảm). Cập nhật `max_len = max(max_len, inc, dec)` tại mỗi bước.",
    "python_starter": get_starter_py("Đoạn Con #3"),
    "c_starter": get_starter_c("Đoạn Con #3"),
    "solution_python": """import sys

def solve():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    nums = [int(x) for x in tokens[1:n+1]]
    if n <= 1:
        print(n)
        return
    max_len = 1
    inc = 1
    dec = 1
    for i in range(1, n):
        if nums[i] > nums[i - 1]:
            inc += 1
            dec = 1
        elif nums[i] < nums[i - 1]:
            dec += 1
            inc = 1
        else:
            inc = 1
            dec = 1
        if inc > max_len:
            max_len = inc
        if dec > max_len:
            max_len = dec
    print(max_len)

if __name__ == '__main__':
    solve()""",
    "solution_c": """#include <stdio.h>

int main() {
    int n;
    if (scanf("%d", &n) == 1) {
        if (n <= 1) {
            printf("%d\\n", n);
            return 0;
        }
        long long a[1005];
        for (int i = 0; i < n; i++) {
            scanf("%lld", &a[i]);
        }
        int max_len = 1, inc = 1, dec = 1;
        for (int i = 1; i < n; i++) {
            if (a[i] > a[i - 1]) {
                inc++;
                dec = 1;
            } else if (a[i] < a[i - 1]) {
                dec++;
                inc = 1;
            } else {
                inc = 1;
                dec = 1;
            }
            if (inc > max_len) max_len = inc;
            if (dec > max_len) max_len = dec;
        }
        printf("%d\\n", max_len);
    }
    return 0;
}""",
    "editorial": "### Phân Tích & Hướng Dẫn Giải\\n- **Ý tưởng:** Đoạn con đơn điệu nghiêm ngặt liên tiếp có thể là tăng dần ($a_i < a_{i+1}$) hoặc giảm dần ($a_i > a_{i+1}$). Ta duyệt mảng từ vị trí thứ hai: nếu $a_i > a_{i-1}$, tăng chuỗi tăng `inc += 1` và reset chuỗi giảm `dec = 1`; nếu $a_i < a_{i-1}$, tăng chuỗi giảm `dec += 1` và reset `inc = 1`; nếu bằng nhau thì cả hai chuỗi đều reset về 1.\\n- **Độ phức tạp:** Thời gian $O(n)$, Bộ nhớ $O(n)$ hoặc $O(1)$.",
    "test_cases": [
        {"test_index": 1, "is_sample": True, "description": "Test cơ bản (Mẫu)", "input_data": "8\n1 2 2 -2 -2 2 3 5\n", "expected_output": "4\n"},
        {"test_index": 2, "is_sample": True, "description": "Mảng giảm nghiêm ngặt", "input_data": "5\n5 4 3 2 1\n", "expected_output": "5\n"},
        {"test_index": 3, "is_sample": False, "description": "Tất cả các số bằng nhau", "input_data": "4\n2 2 2 2\n", "expected_output": "1\n"},
        {"test_index": 4, "is_sample": False, "description": "Mảng chỉ 1 phần tử", "input_data": "1\n42\n", "expected_output": "1\n"},
        {"test_index": 5, "is_sample": False, "description": "Đoạn giảm dài ở đuôi", "input_data": "7\n1 3 5 2 1 0 -1\n", "expected_output": "5\n"}
    ]
})

# 91: ĐOẠN CON #4
chunk_86_100.append({
    "id": "DRAGON-91",
    "title": "Đoạn Con #4 (Âm Dương Đan Xen)",
    "chapter": "Phần VIII. Mảng một chiều cơ bản",
    "difficulty": "Dễ",
    "time_limit": 1.5,
    "memory_limit": 256,
    "description": "Nhập vào mảng $A$ gồm $n$ số nguyên khác 0. Tìm độ dài của đoạn con liên tiếp dài nhất chứa các phần tử âm dương đan xen nhau (hai phần tử liền kề trái dấu: $a_i \\times a_{i+1} < 0$).",
    "input_format": "Dòng 1: Số nguyên dương $n$ ($1 \\le n \\le 1000$).\\nDòng 2: $n$ số nguyên khác 0 của mảng $A$ ($-10^6 \\le a_i \\le 10^6$), cách nhau bởi khoảng trắng.",
    "output_format": "In ra số lượng phần tử của đoạn con tìm được.",
    "constraints": "$1 \\le n \\le 1000$\\n$-10^6 \\le a_i \\le 10^6, a_i \\ne 0$\\nThời gian chạy: 1.5s\\nBộ nhớ: 256MB",
    "sample_input": "8\n1 2 2 -2 3 -4 3 3",
    "sample_output": "5",
    "hints": "Kiểm tra hai phần tử liền kề có trái dấu không bằng điều kiện $(a_i > 0 \\land a_{i-1} < 0) \\lor (a_i < 0 \\land a_{i-1} > 0)$.",
    "python_starter": get_starter_py("Đoạn Con #4"),
    "c_starter": get_starter_c("Đoạn Con #4"),
    "solution_python": """import sys

def solve():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    nums = [int(x) for x in tokens[1:n+1]]
    if n == 0:
        print(0)
        return
    max_len = 1
    cur = 1
    for i in range(1, n):
        if (nums[i] > 0 and nums[i - 1] < 0) or (nums[i] < 0 and nums[i - 1] > 0):
            cur += 1
        else:
            cur = 1
        if cur > max_len:
            max_len = cur
    print(max_len)

if __name__ == '__main__':
    solve()""",
    "solution_c": """#include <stdio.h>

int main() {
    int n;
    if (scanf("%d", &n) == 1) {
        if (n == 0) {
            printf("0\\n");
            return 0;
        }
        long long a[1005];
        for (int i = 0; i < n; i++) scanf("%lld", &a[i]);
        int max_len = 1, cur = 1;
        for (int i = 1; i < n; i++) {
            if ((a[i] > 0 && a[i - 1] < 0) || (a[i] < 0 && a[i - 1] > 0)) {
                cur++;
            } else {
                cur = 1;
            }
            if (cur > max_len) max_len = cur;
        }
        printf("%d\\n", max_len);
    }
    return 0;
}""",
    "editorial": "### Phân Tích & Hướng Dẫn Giải\\n- **Ý tưởng:** Duyệt tuần tự qua mảng $A$. So sánh phần tử hiện tại $a_i$ với phần tử đứng trước $a_{i-1}$. Nếu hai phần tử trái dấu (một dương, một âm), đoạn con đan xen kéo dài thêm 1 đơn vị. Ngược lại nếu cùng dấu, đoạn con đan xen bắt đầu lại từ $a_i$ với độ dài 1.\\n- **Độ phức tạp:** Thời gian $O(n)$, Bộ nhớ $O(1)$.",
    "test_cases": [
        {"test_index": 1, "is_sample": True, "description": "Test cơ bản (Mẫu 1)", "input_data": "8\n1 2 2 -2 3 -4 3 3\n", "expected_output": "5\n"},
        {"test_index": 2, "is_sample": True, "description": "Test mẫu 2", "input_data": "8\n-1 -2 1 -3 -1 4 -5 5\n", "expected_output": "4\n"},
        {"test_index": 3, "is_sample": False, "description": "Toàn bộ cùng dấu dương", "input_data": "4\n1 2 3 4\n", "expected_output": "1\n"},
        {"test_index": 4, "is_sample": False, "description": "Đan xen hoàn hảo từ đầu đến cuối", "input_data": "5\n1 -1 1 -1 1\n", "expected_output": "5\n"},
        {"test_index": 5, "is_sample": False, "description": "Mảng 1 phần tử", "input_data": "1\n-7\n", "expected_output": "1\n"}
    ]
})

# 92: ĐOẠN CON #5
chunk_86_100.append({
    "id": "DRAGON-92",
    "title": "Đoạn Con #5 (Chia Hết Cho K)",
    "chapter": "Phần VIII. Mảng một chiều cơ bản",
    "difficulty": "Dễ",
    "time_limit": 1.5,
    "memory_limit": 256,
    "description": "Nhập vào mảng $A$ gồm $n$ phần tử và số nguyên dương $k$. Tìm độ dài của đoạn con liên tiếp dài nhất chứa các phần tử chia hết cho $k$ ($a_i \\% k == 0$).",
    "input_format": "Dòng 1: Hai số nguyên dương $n$ và $k$ ($1 \\le n \\le 1000, 1 \\le k \\le 1000$).\\nDòng 2: $n$ số nguyên $a_i$ ($-10^6 \\le a_i \\le 10^6$), cách nhau bởi khoảng trắng.",
    "output_format": "In ra độ dài lớn nhất của đoạn con tìm được (in 0 nếu không có phần tử nào chia hết cho $k$).",
    "constraints": "$1 \\le n \\le 1000$\\n$1 \\le k \\le 1000$\\n$-10^6 \\le a_i \\le 10^6$\\nThời gian chạy: 1.5s\\nBộ nhớ: 256MB",
    "sample_input": "8 2\n1 2 2 -2 6 -4 3 3",
    "sample_output": "5",
    "hints": "Duyệt qua mảng: nếu $a_i \\% k == 0$, tăng biến đếm đoạn hiện tại; ngược lại reset về 0.",
    "python_starter": get_starter_py("Đoạn Con #5"),
    "c_starter": get_starter_c("Đoạn Con #5"),
    "solution_python": """import sys

def solve():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n, k = int(tokens[0]), int(tokens[1])
    nums = [int(x) for x in tokens[2:n+2]]
    max_len = 0
    cur = 0
    for x in nums:
        if x % k == 0:
            cur += 1
            if cur > max_len:
                max_len = cur
        else:
            cur = 0
    print(max_len)

if __name__ == '__main__':
    solve()""",
    "solution_c": """#include <stdio.h>

int main() {
    int n, k;
    if (scanf("%d %d", &n, &k) == 2) {
        int max_len = 0, cur = 0;
        for (int i = 0; i < n; i++) {
            long long x;
            if (scanf("%lld", &x) == 1) {
                if (x % k == 0) {
                    cur++;
                    if (cur > max_len) max_len = cur;
                } else {
                    cur = 0;
                }
            }
        }
        printf("%d\\n", max_len);
    }
    return 0;
}""",
    "editorial": "### Phân Tích & Hướng Dẫn Giải\\n- **Ý tưởng:** Duyệt mảng tuần tự. Mỗi khi gặp phần tử chia hết cho $k$ ($x \\% k == 0$), tăng độ dài chuỗi liên tiếp `cur` và cập nhật `max_len`. Nếu không chia hết, đặt `cur = 0`.\\n- **Độ phức tạp:** Thời gian $O(n)$, Bộ nhớ $O(1)$.",
    "test_cases": [
        {"test_index": 1, "is_sample": True, "description": "Test cơ bản (Mẫu 1)", "input_data": "8 2\n1 2 2 -2 6 -4 3 3\n", "expected_output": "5\n"},
        {"test_index": 2, "is_sample": True, "description": "Không có phần tử nào chia hết (Mẫu 2)", "input_data": "8 6\n-1 -2 1 -3 -1 4 -5 5\n", "expected_output": "0\n"},
        {"test_index": 3, "is_sample": False, "description": "Mọi phần tử đều chia hết", "input_data": "5 3\n3 6 9 12 15\n", "expected_output": "5\n"},
        {"test_index": 4, "is_sample": False, "description": "Không phần tử nào chia hết", "input_data": "4 5\n1 2 3 4\n", "expected_output": "0\n"},
        {"test_index": 5, "is_sample": False, "description": "Có số 0 (0 chia hết cho mọi k)", "input_data": "6 10\n10 20 0 30 4 50\n", "expected_output": "4\n"}
    ]
})

# 93: PHÂN SỐ
chunk_86_100.append({
    "id": "DRAGON-93",
    "title": "Phân Số Đơn Vị (1/x = 1/a + 1/b + 1/c)",
    "chapter": "Phần V. Bài toán phân tích & Số học",
    "difficulty": "Trung bình",
    "time_limit": 1.5,
    "memory_limit": 256,
    "description": "Nhập vào số nguyên dương $x$. Hãy tìm 3 số nguyên dương $a, b, c$ sao cho:\\n$$\\frac{1}{x} = \\frac{1}{a} + \\frac{1}{b} + \\frac{1}{c} \\quad (a \\le b \\le c)$$\\nÁp dụng hằng đẳng thức kinh điển phân tích phân số: $\\frac{1}{2} + \\frac{1}{3} + \\frac{1}{6} = 1 \\implies \\frac{1}{x} = \\frac{1}{2x} + \\frac{1}{3x} + \\frac{1}{6x}$.",
    "input_format": "Một dòng duy nhất ghi số nguyên dương $x$ ($1 \\le x \\le 10000$).",
    "output_format": "Ba số nguyên dương $a, b, c$ cách nhau một khoảng trắng ($a \\le b \\le c$).",
    "constraints": "$1 \\le x \\le 10000$\\nThời gian chạy: 1.5s\\nBộ nhớ: 256MB",
    "sample_input": "5",
    "sample_output": "10 15 30",
    "hints": "Sử dụng công thức tổng quát $a = 2x, b = 3x, c = 6x$. Ta luôn có $1/(2x) + 1/(3x) + 1/(6x) = 1/x$.",
    "python_starter": get_starter_py("Phân Số"),
    "c_starter": get_starter_c("Phân Số"),
    "solution_python": """import sys

def solve():
    line = sys.stdin.read().strip()
    if not line:
        return
    x = int(line)
    print(f"{2 * x} {3 * x} {6 * x}")

if __name__ == '__main__':
    solve()""",
    "solution_c": """#include <stdio.h>

int main() {
    long long x;
    if (scanf("%lld", &x) == 1) {
        printf("%lld %lld %lld\\n", 2 * x, 3 * x, 6 * x);
    }
    return 0;
}""",
    "editorial": "### Phân Tích & Hướng Dẫn Giải\\n- **Ý tưởng:** Với mọi số nguyên dương $x$, ta nhận thấy $1/2 + 1/3 + 1/6 = 3/6 + 2/6 + 1/6 = 6/6 = 1$. Khi chia cả hai vế cho $x$, ta thu được đẳng thức đẹp mắt:\\n$$\\frac{1}{x} = \\frac{1}{2x} + \\frac{1}{3x} + \\frac{1}{6x}$$\\nVới $a = 2x, b = 3x, c = 6x$, ba số này luôn là số nguyên dương và thỏa mãn $a \\le b \\le c$.\\n- **Độ phức tạp:** Thời gian $O(1)$, Bộ nhớ $O(1)$.",
    "test_cases": [
        {"test_index": 1, "is_sample": True, "description": "Test cơ bản (Mẫu x = 5)", "input_data": "5\n", "expected_output": "10 15 30\n"},
        {"test_index": 2, "is_sample": True, "description": "Biên dưới (x = 1)", "input_data": "1\n", "expected_output": "2 3 6\n"},
        {"test_index": 3, "is_sample": False, "description": "Test x = 2", "input_data": "2\n", "expected_output": "4 6 12\n"},
        {"test_index": 4, "is_sample": False, "description": "Test x = 10", "input_data": "10\n", "expected_output": "20 30 60\n"},
        {"test_index": 5, "is_sample": False, "description": "Biên trên x = 10000", "input_data": "10000\n", "expected_output": "20000 30000 60000\n"}
    ]
})

# 94 from existing
chunk_86_100.append(existing_dict["DRAGON-94"])

# 95: TỔNG LIÊN TIẾP
chunk_86_100.append({
    "id": "DRAGON-95",
    "title": "Tổng Liên Tiếp (Phân Tích Thành Tổng)",
    "chapter": "Phần V. Bài toán phân tích & Số học",
    "difficulty": "Trung bình",
    "time_limit": 1.5,
    "memory_limit": 256,
    "description": "Nhập vào số nguyên dương $n$. Hãy tìm cách phân tích $n$ thành tổng các số nguyên dương liên tiếp (ít nhất 2 số). Dữ liệu đảm bảo luôn có thể phân tích được. Nếu có nhiều cách phân tích, chọn cách có nhiều số hạng nhất (bắt đầu từ số nhỏ nhất).",
    "input_format": "Một dòng ghi số nguyên dương $n$ ($1 \\le n \\le 1000000$).",
    "output_format": "In ra các số nguyên dương liên tiếp có tổng bằng $n$, các số từ bé đến lớn cách nhau 1 dấu cách.",
    "constraints": "$1 \\le n \\le 10^6$\\nThời gian chạy: 1.5s\\nBộ nhớ: 256MB",
    "sample_input": "10",
    "sample_output": "1 2 3 4",
    "hints": "Nếu tổng có $k$ số bắt đầu từ $s$, ta có công thức: $k \\times s + k(k-1)/2 = n$. Duyệt $k$ từ giá trị lớn nhất giảm dần về 2.",
    "python_starter": get_starter_py("Tổng Liên Tiếp"),
    "c_starter": get_starter_c("Tổng Liên Tiếp"),
    "solution_python": """import sys
import math

def solve():
    line = sys.stdin.read().strip()
    if not line:
        return
    n = int(line)
    max_k = int(math.isqrt(2 * n)) + 2
    for k in range(max_k, 1, -1):
        rem = n - k * (k - 1) // 2
        if rem > 0 and rem % k == 0:
            s = rem // k
            res = [str(s + i) for i in range(k)]
            print(" ".join(res))
            return
    print(n)

if __name__ == '__main__':
    solve()""",
    "solution_c": """#include <stdio.h>
#include <math.h>

int main() {
    long long n;
    if (scanf("%lld", &n) == 1) {
        long long max_k = (long long)sqrt(2 * n) + 2;
        for (long long k = max_k; k >= 2; k--) {
            long long rem = n - k * (k - 1) / 2;
            if (rem > 0 && rem % k == 0) {
                long long s = rem / k;
                for (long long i = 0; i < k; i++) {
                    printf("%lld%c", s + i, (i == k - 1) ? '\\n' : ' ');
                }
                return 0;
            }
        }
        printf("%lld\\n", n);
    }
    return 0;
}""",
    "editorial": "### Phân Tích & Hướng Dẫn Giải\\n- **Ý tưởng:** Giả sử $n$ được biểu diễn thành tổng của $k$ số nguyên dương liên tiếp bắt đầu từ $s$: $n = s + (s+1) + \\dots + (s+k-1) = k \\cdot s + \\frac{k(k-1)}{2}$.\\n- Ta suy ra: $k \\cdot s = n - \\frac{k(k-1)}{2}$. Để tìm cách phân tích có nhiều số hạng nhất, ta cho $k$ giảm dần từ $\\sqrt{2n}$ về $2$. Giá trị $k$ đầu tiên thỏa mãn $n - k(k-1)/2 > 0$ và chia hết cho $k$ sẽ cho dãy dài nhất.\\n- **Độ phức tạp:** Thời gian $O(\\sqrt{n})$, Bộ nhớ $O(1)$.",
    "test_cases": [
        {"test_index": 1, "is_sample": True, "description": "Test cơ bản (Mẫu n = 10 -> 1 2 3 4)", "input_data": "10\n", "expected_output": "1 2 3 4\n"},
        {"test_index": 2, "is_sample": True, "description": "Test n = 15 (1 2 3 4 5)", "input_data": "15\n", "expected_output": "1 2 3 4 5\n"},
        {"test_index": 3, "is_sample": False, "description": "Test n = 3 (1 2)", "input_data": "3\n", "expected_output": "1 2\n"},
        {"test_index": 4, "is_sample": False, "description": "Test n = 21 (1 2 3 4 5 6)", "input_data": "21\n", "expected_output": "1 2 3 4 5 6\n"},
        {"test_index": 5, "is_sample": False, "description": "Test n = 100 (9 10 11 12 13 14 15 16)", "input_data": "100\n", "expected_output": "9 10 11 12 13 14 15 16\n"}
    ]
})

# 96: PHẦN TỬ YÊN NGỰA
chunk_86_100.append({
    "id": "DRAGON-96",
    "title": "Phần Tử Yên Ngựa (Saddle Point)",
    "chapter": "Phần IX. Mảng hai chiều & Ma trận",
    "difficulty": "Trung bình",
    "time_limit": 1.5,
    "memory_limit": 256,
    "description": "Nhập vào ma trận $A$ kích thước $n \\times m$. In ra số lượng các phần tử yên ngựa trong ma trận.\\nMột phần tử $a[i, j]$ được coi là phần tử yên ngựa khi nó đồng thời là phần tử nhỏ nhất của hàng $i$ và là phần tử lớn nhất của cột $j$.",
    "input_format": "Dòng 1: Hai số nguyên dương $n, m$ ($1 \\le n, m \\le 20$).\\n$n$ dòng tiếp theo, mỗi dòng là $m$ số nguyên trong khoảng $[-1000, 1000]$.",
    "output_format": "In ra số lượng phần tử yên ngựa tìm được.",
    "constraints": "$1 \\le n, m \\le 20$\\n$-1000 \\le a[i, j] \\le 1000$\\nThời gian chạy: 1.5s\\nBộ nhớ: 256MB",
    "sample_input": "3 4\n4 4 4 5\n5 6 4 8\n5 8 5 7",
    "sample_output": "2",
    "hints": "Tính trước mảng giá trị nhỏ nhất của mỗi hàng `row_min[i]` và giá trị lớn nhất của mỗi cột `col_max[j]`. Sau đó đếm các vị trí $(i, j)$ có $a[i][j] == row\\_min[i] == col\\_max[j]$.",
    "python_starter": get_starter_py("Phần Tử Yên Ngựa"),
    "c_starter": get_starter_c("Phần Tử Yên Ngựa"),
    "solution_python": """import sys

def solve():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n, m = int(tokens[0]), int(tokens[1])
    idx = 2
    matrix = []
    for _ in range(n):
        matrix.append([int(x) for x in tokens[idx:idx+m]])
        idx += m
    row_mins = [min(row) for row in matrix]
    col_maxs = [max(matrix[r][c] for r in range(n)) for c in range(m)]
    count = 0
    for r in range(n):
        for c in range(m):
            if matrix[r][c] == row_mins[r] and matrix[r][c] == col_maxs[c]:
                count += 1
    print(count)

if __name__ == '__main__':
    solve()""",
    "solution_c": """#include <stdio.h>

int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) == 2) {
        int a[25][25];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                scanf("%d", &a[i][j]);
            }
        }
        int row_min[25], col_max[25];
        for (int i = 0; i < n; i++) {
            row_min[i] = a[i][0];
            for (int j = 1; j < m; j++) {
                if (a[i][j] < row_min[i]) row_min[i] = a[i][j];
            }
        }
        for (int j = 0; j < m; j++) {
            col_max[j] = a[0][j];
            for (int i = 1; i < n; i++) {
                if (a[i][j] > col_max[j]) col_max[j] = a[i][j];
            }
        }
        int count = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                if (a[i][j] == row_min[i] && a[i][j] == col_max[j]) {
                    count++;
                }
            }
        }
        printf("%d\\n", count);
    }
    return 0;
}""",
    "editorial": "### Phân Tích & Hướng Dẫn Giải\\n- **Ý tưởng:** Đầu tiên, tính trước giá trị nhỏ nhất của mỗi hàng lưu vào mảng `row_min[i]` và giá trị lớn nhất của mỗi cột lưu vào `col_max[j]`. Sau đó, duyệt lại toàn bộ ma trận: phần tử tại $(i, j)$ là điểm yên ngựa nếu $a[i][j] == row\\_min[i]$ và $a[i][j] == col\\_max[j]$.\\n- **Độ phức tạp:** Thời gian $O(n \\times m)$, Bộ nhớ $O(n + m)$.",
    "test_cases": [
        {"test_index": 1, "is_sample": True, "description": "Test cơ bản (Mẫu 3x4)", "input_data": "3 4\n4 4 4 5\n5 6 4 8\n5 8 5 7\n", "expected_output": "2\n"},
        {"test_index": 2, "is_sample": True, "description": "Ma trận 1x1 (luôn là yên ngựa)", "input_data": "1 1\n42\n", "expected_output": "1\n"},
        {"test_index": 3, "is_sample": False, "description": "Ma trận không có yên ngựa", "input_data": "2 2\n1 2\n4 3\n", "expected_output": "0\n"},
        {"test_index": 4, "is_sample": False, "description": "Ma trận toàn phần tử bằng nhau", "input_data": "3 3\n5 5 5\n5 5 5\n5 5 5\n", "expected_output": "9\n"},
        {"test_index": 5, "is_sample": False, "description": "Ma trận đường chéo", "input_data": "3 3\n9 2 3\n4 8 6\n7 5 1\n", "expected_output": "0\n"}
    ]
})

# 97 from existing
chunk_86_100.append(existing_dict["DRAGON-97"])

# 98: GẠCH SỐ #2
chunk_86_100.append({
    "id": "DRAGON-98",
    "title": "Gạch Số #2 (Tạo Số Nhỏ Nhất)",
    "chapter": "Phần X. Kỹ thuật nâng cao & Thuật toán",
    "difficulty": "Trung bình",
    "time_limit": 1.5,
    "memory_limit": 256,
    "description": "Cho xâu ký tự số $S$. Hãy gạch đi $k$ chữ số bất kỳ sao cho các chữ số còn lại theo thứ tự ban đầu tạo thành số có giá trị nhỏ nhất có thể.",
    "input_format": "Dòng 1: Số nguyên dương $k$ (nhỏ hơn độ dài của xâu $S$).\\nDòng 2: Xâu $S$ gồm các ký tự chữ số từ '0' đến '9' (độ dài không quá 100).",
    "output_format": "In ra xâu $S$ sau khi xoá $k$ chữ số.",
    "constraints": "$1 \\le k < |S| \\le 100$\\nThời gian chạy: 1.5s\\nBộ nhớ: 256MB",
    "sample_input": "3\n23571113",
    "sample_output": "21113",
    "hints": "Sử dụng cấu trúc ngăn xếp (Monotonic Stack): khi duyệt chữ số mới nhỏ hơn đỉnh ngăn xếp và còn lượt xóa $k$, ta pop đỉnh ngăn xếp ra.",
    "python_starter": get_starter_py("Gạch Số #2"),
    "c_starter": get_starter_c("Gạch Số #2"),
    "solution_python": """import sys

def solve():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    k = int(tokens[0])
    s = tokens[1]
    stack = []
    k_left = k
    for ch in s:
        while stack and stack[-1] > ch and k_left > 0:
            stack.pop()
            k_left -= 1
        stack.append(ch)
    if k_left > 0:
        stack = stack[:-k_left]
    print("".join(stack))

if __name__ == '__main__':
    solve()""",
    "solution_c": """#include <stdio.h>
#include <string.h>

int main() {
    int k;
    char s[205];
    if (scanf("%d %s", &k, s) == 2) {
        char stack[205];
        int top = 0;
        int k_left = k;
        int len = strlen(s);
        for (int i = 0; i < len; i++) {
            while (top > 0 && stack[top - 1] > s[i] && k_left > 0) {
                top--;
                k_left--;
            }
            stack[top++] = s[i];
        }
        top -= k_left;
        stack[top] = '\\0';
        printf("%s\\n", stack);
    }
    return 0;
}""",
    "editorial": "### Phân Tích & Hướng Dẫn Giải\\n- **Ý tưởng:** Để số tạo thành là nhỏ nhất, các chữ số ở hàng cao hơn phải càng nhỏ càng tốt. Ta dùng kỹ thuật Monotonic Stack tăng dần: duyệt từng ký tự chữ số của $S$, nếu chữ số đỉnh stack lớn hơn chữ số hiện tại và vẫn còn lượt xóa ($k > 0$), ta loại bỏ đỉnh stack.\\n- Nếu sau khi duyệt hết chuỗi mà vẫn còn lượt xóa $k$, ta cắt bỏ $k$ ký tự cuối cùng của stack.\\n- **Độ phức tạp:** Thời gian $O(|S|)$, Bộ nhớ $O(|S|)$.",
    "test_cases": [
        {"test_index": 1, "is_sample": True, "description": "Test cơ bản (Mẫu)", "input_data": "3\n23571113\n", "expected_output": "21113\n"},
        {"test_index": 2, "is_sample": True, "description": "Dãy giảm dần xoá hết số lớn", "input_data": "3\n987654\n", "expected_output": "654\n"},
        {"test_index": 3, "is_sample": False, "description": "Dãy tăng dần xoá ở đuôi", "input_data": "2\n12345\n", "expected_output": "123\n"},
        {"test_index": 4, "is_sample": False, "description": "Có số 0 ở giữa", "input_data": "2\n10200\n", "expected_output": "0200\n"},
        {"test_index": 5, "is_sample": False, "description": "Chuỗi dài xoá nhiều số", "input_data": "4\n43214321\n", "expected_output": "121\n"}
    ]
})

# 99: SẮP XẾP XOẮN ỐC
chunk_86_100.append({
    "id": "DRAGON-99",
    "title": "Sắp Xếp Xoắn Ốc (Spiral Sort)",
    "chapter": "Phần IX. Mảng hai chiều & Ma trận",
    "difficulty": "Trung bình",
    "time_limit": 1.5,
    "memory_limit": 256,
    "description": "Cho mảng hai chiều $A$ kích thước $n \\times m$. Hãy sắp xếp tất cả các phần tử trong mảng $A$ theo thứ tự tăng dần theo chiều kim đồng hồ (xoắn ốc từ ngoài vào trong).",
    "input_format": "Dòng 1: Hai số nguyên dương $n, m$ ($1 \\le n, m \\le 20$).\\n$n$ dòng tiếp theo, mỗi dòng ghi $m$ số nguyên trong khoảng $[-1000, 1000]$.",
    "output_format": "In ra mảng $A$ sau khi sắp xếp xoắn ốc (gồm $n$ dòng, mỗi dòng $m$ số cách nhau bởi một khoảng trắng).",
    "constraints": "$1 \\le n, m \\le 20$\\n$-1000 \\le a[i, j] \\le 1000$\\nThời gian chạy: 1.5s\\nBộ nhớ: 256MB",
    "sample_input": "4 4\n4 5 7 1\n21 32 10 6\n3 2 9 11\n13 20 34 67",
    "sample_output": "1 2 3 4\n20 21 32 5\n13 67 34 6\n11 10 9 7",
    "hints": "Thu thập tất cả $n \\times m$ phần tử vào một mảng 1D rồi sắp xếp tăng dần. Sau đó điền tuần tự các phần tử vào ma trận theo 4 đường biên (trên, phải, dưới, trái).",
    "python_starter": get_starter_py("Sắp Xếp Xoắn Ốc"),
    "c_starter": get_starter_c("Sắp Xếp Xoắn Ốc"),
    "solution_python": """import sys

def solve():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n, m = int(tokens[0]), int(tokens[1])
    vals = sorted([int(x) for x in tokens[2:2 + n * m]])
    res = [[0] * m for _ in range(n)]
    top, bottom, left, right = 0, n - 1, 0, m - 1
    idx = 0
    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            res[top][c] = vals[idx]
            idx += 1
        top += 1
        for r in range(top, bottom + 1):
            res[r][right] = vals[idx]
            idx += 1
        right -= 1
        if top <= bottom:
            for c in range(right, left - 1, -1):
                res[bottom][c] = vals[idx]
                idx += 1
            bottom -= 1
        if left <= right:
            for r in range(bottom, top - 1, -1):
                res[r][left] = vals[idx]
                idx += 1
            left += 1
    for row in res:
        print(" ".join(map(str, row)))

if __name__ == '__main__':
    solve()""",
    "solution_c": """#include <stdio.h>
#include <stdlib.h>

int cmp(const void *a, const void *b) {
    return (*(int*)a - *(int*)b);
}

int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) == 2) {
        int total = n * m;
        int *vals = (int*)malloc(total * sizeof(int));
        for (int i = 0; i < total; i++) {
            scanf("%d", &vals[i]);
        }
        qsort(vals, total, sizeof(int), cmp);
        int res[25][25];
        int top = 0, bottom = n - 1, left = 0, right = m - 1;
        int idx = 0;
        while (top <= bottom && left <= right) {
            for (int c = left; c <= right; c++) res[top][c] = vals[idx++];
            top++;
            for (int r = top; r <= bottom; r++) res[r][right] = vals[idx++];
            right--;
            if (top <= bottom) {
                for (int c = right; c >= left; c--) res[bottom][c] = vals[idx++];
                bottom--;
            }
            if (left <= right) {
                for (int r = bottom; r >= top; r--) res[r][left] = vals[idx++];
                left++;
            }
        }
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                printf("%d%c", res[i][j], (j == m - 1) ? '\\n' : ' ');
            }
        }
        free(vals);
    }
    return 0;
}""",
    "editorial": "### Phân Tích & Hướng Dẫn Giải\\n- **Ý tưởng:** Đọc toàn bộ $n \\times m$ phần tử vào mảng và sắp xếp tăng dần. Ta dùng 4 con trỏ giới hạn vùng ma trận chưa điền: `top = 0, bottom = n - 1, left = 0, right = m - 1`. Lần lượt điền theo 4 hướng kim đồng hồ: từ trái sang phải ở hàng `top`, từ trên xuống dưới ở cột `right`, từ phải sang trái ở hàng `bottom`, và từ dưới lên trên ở cột `left`.\\n- **Độ phức tạp:** Thời gian $O((n m) \\log(n m))$, Bộ nhớ $O(n m)$.",
    "test_cases": [
        {"test_index": 1, "is_sample": True, "description": "Test cơ bản (Mẫu 4x4)", "input_data": "4 4\n4 5 7 1\n21 32 10 6\n3 2 9 11\n13 20 34 67\n", "expected_output": "1 2 3 4\n20 21 32 5\n13 67 34 6\n11 10 9 7\n"},
        {"test_index": 2, "is_sample": True, "description": "Ma trận 1x1", "input_data": "1 1\n99\n", "expected_output": "99\n"},
        {"test_index": 3, "is_sample": False, "description": "Ma trận 2x2", "input_data": "2 2\n4 2\n1 3\n", "expected_output": "1 2\n4 3\n"},
        {"test_index": 4, "is_sample": False, "description": "Ma trận 1 hàng 3 cột", "input_data": "1 3\n3 1 2\n", "expected_output": "1 2 3\n"},
        {"test_index": 5, "is_sample": False, "description": "Ma trận 3 hàng 1 cột", "input_data": "3 1\n8\n2\n5\n", "expected_output": "2\n5\n8\n"}
    ]
})

# 100 from existing
chunk_86_100.append(existing_dict["DRAGON-100"])

with open('data_generators/problems_86_100.py', 'w', encoding='utf-8') as f:
    f.write('problems = ' + repr(chunk_86_100) + '\n')

print(f"Generated data_generators/problems_86_100.py with {len(chunk_86_100)} problems!")
