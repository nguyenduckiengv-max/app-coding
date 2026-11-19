# 🐉 BÍ KÍP LUYỆN RỒNG - ONLINE CODE JUDGE PLATFORM
> **"Đã code là fun • Càng code càng fun"**  
> Nền tảng luyện lập trình cá nhân mô phỏng LeetCode / HackerRank / Codefun dành riêng cho tuyển tập kinh điển **"Bí kíp luyện rồng - Bài tập lập trình cho người mới học"** (Chuyên KHTN & UET VNU).

---

## 🌟 1. TỔNG QUAN KIẾN TRÚC HỆ THỐNG

Ứng dụng được thiết kế theo kiến trúc Full-stack hiện đại, phân tách rõ ràng giữa Web Application, Storage, Security Sandbox và Execution Engine:

```
c:\wweb luyen code\
├── app.py                      # Flask Application Server & REST API endpoints
├── config.py                   # Cấu hình hệ thống (Timeout 1.5s, GCC flags, đường dẫn)
├── requirements.txt            # Danh sách thư viện Python phụ thuộc (Flask)
│
├── judge/                      # Hệ thống chấm điểm tự động (Judge Engine)
│   ├── __init__.py
│   ├── security.py             # Bộ lọc mã độc Sandbox (AST check cho Python, regex cho C)
│   └── engine.py               # Biên dịch C (GCC 16), thực thi Python 3, chuẩn hóa output, chấm điểm
│
├── models/                     # Quản trị Cơ sở dữ liệu SQLite
│   ├── __init__.py
│   └── database.py             # Quản lý bảng problems, test_cases, submissions và thống kê
│
├── data/                       # Dữ liệu đề bài & bộ test cases
│   ├── dragon_judge.db         # Database SQLite lưu trữ lịch sử nộp và thống kê
│   └── problems.json           # Master JSON chứa danh sách bài tập & bộ 5 test cases chuẩn
│
├── templates/                  # Giao diện HTML5 (Jinja2)
│   ├── base.html               # Layout chuẩn với Tailwind CSS, Lucide icons, KaTeX toán học
│   ├── index.html              # Trang danh mục bài tập, bộ lọc đa năng, bảng thống kê
│   ├── problem.html            # Giao diện luyện code 2 cột LeetCode / HackerRank
│   └── guide.html              # Trang hướng dẫn chi tiết cách thêm bài tập và cơ chế chấm
│
├── static/                     # Tài nguyên tĩnh
│   ├── css/
│   │   └── custom.css          # Tùy biến thanh cuộn, giao diện Monaco, badge
│   └── js/
│       └── editor.js           # Tích hợp Monaco Editor (VS Code), phím tắt, AJAX Run/Submit
│
└── README.md                   # Tài liệu hướng dẫn toàn diện
```

---

## 🚀 2. TÍNH NĂNG NỔI BẬT

### 2.1. Giao diện 2 cột chuẩn LeetCode / HackerRank
- **Cột bên trái:**
  - Tab **Đề bài**: Hiển thị mô tả bài toán, định dạng Input/Output, Ràng buộc dữ liệu và Ví dụ mẫu (Sample Test) kèm nút 1-click sao chép.
  - Tab **Lịch sử nộp bài**: Theo dõi tiến trình cá nhân (AC, WA, TLE, CE, điểm số, thời gian thực thi ms).
  - Tab **Gợi ý**: Cung cấp gợi ý giải nhanh và lưu ý các bẫy tràn số hay độ phức tạp.
  - Tab **Lời Giải (Solution / Editorial)**: Được thiết kế theo cơ chế HackerRank. Khung code ban đầu là template rỗng; sau khi người dùng nộp bài (Submit) hoặc xác nhận mở khóa, tab Lời Giải sẽ hiển thị:
    + Ý tưởng thuật toán và phân tích độ phức tạp thời gian/bộ nhớ ($O(N)$, $O(1)$).
    + Mã nguồn giải chuẩn bằng **Python 3** (kèm nút Copy và nút nạp code vào Editor).
    + Mã nguồn giải chuẩn bằng **C (GCC)** (kèm nút Copy và nút nạp code vào Editor).
- **Cột bên phải:**
  - **Monaco Code Editor**: Bộ soạn thảo mã nguồn tương tự Visual Studio Code với cú pháp màu, gợi ý code, tự động căn lề, line numbers. Khởi đầu với khung sườn rỗng (clean boilerplate), không làm lộ đáp án trước khi người dùng làm bài!
  - Hỗ trợ đổi ngôn ngữ linh hoạt giữa **Python 3** và **C (GCC 16 - C11)**.
  - **Console Drawer**:
    - Tab *Test Mẫu (Stdin)*: Cho phép nhập dữ liệu tùy ý để chạy thử trước khi nộp.
    - Tab *Kết Quả Chạy Thử*: Hiển thị đầu ra STDOUT / STDERR và thời gian chạy ms.
    - Tab *Kết Quả Chấm Điểm*: Bảng tổng quan điểm số (100/100), nút xem Editorial và thẻ phân tích chi tiết từng test case trong bộ 5 test cases.

### 2.2. Hệ thống Test Case & Chấm điểm tự động (Judge Engine)
Mỗi bài tập được trang bị bộ tối thiểu **5 test cases** bao quát toàn diện:
1. **Test 1 & Test 2:** Test cơ bản khớp theo ví dụ mẫu trong sách "Bí kíp luyện rồng".
2. **Test 3:** Test giá trị biên (số `0`, số âm, chuỗi $1$ ký tự, mảng biên nhỏ nhất/lớn nhất).
3. **Test 4 & Test 5:** Stress test với dữ liệu cực đại ($10^9$) để kiểm tra độ tối ưu thuật toán tránh TLE và kiểm tra khả năng tràn số 32-bit (`long long` trong C).

#### Các mã kết quả chấm:
- `AC (Accepted)`: Kết quả chính xác hoàn toàn (100% test cases vượt qua).
- `WA (Wrong Answer)`: Kết quả đầu ra khác với đáp án chuẩn.
- `TLE (Time Limit Exceeded)`: Chạy quá giới hạn thời gian (mặc định $1.5$ giây).
- `CE (Compilation Error)`: Lỗi biên dịch trong ngôn ngữ C (hiển thị chi tiết lỗi của GCC).
- `RTE (Runtime Error)`: Chương trình bị lỗi thực thi hoặc kết thúc với mã lỗi khác 0.
- `SECURITY_VIOLATION`: Mã nguồn chứa các hàm hoặc thư viện nguy hiểm bị chặn bởi Sandbox.

### 2.3. Cơ chế Sandbox & An toàn mã nguồn
- **Phân tích cú pháp trừu tượng (Python AST Check):** Quét cây cú pháp của mã Python, chủ động chặn các import nguy hiểm như `os`, `subprocess`, `socket`, `shutil`, `ctypes`, `urllib` và các hàm `eval`, `exec`, `__import__`.
- **Bộ lọc mã nguồn C:** Chặn các header can thiệp hệ thống như `<windows.h>`, `<winsock.h>`, `<unistd.h>` và các lời gọi `system()`, `popen()`, `fork()`, `exec()`.
- **Thư mục thực thi cô lập:** Mỗi lượt chạy được sinh mã UUID riêng trong `temp_exec/`, hoàn toàn cách ly và được xóa sạch ngay sau khi có kết quả.
- **Giới hạn thời gian (Timeout):** Mỗi lần chạy bị ép ngắt sau $1.5$ giây để triệt tiêu các vòng lặp vô tận.

---

## 🛠️ 3. HƯỚNG DẪN CÀI ĐẶT & CHẠY ỨNG DỤNG

### Bước 1: Yêu cầu môi trường
- **Python**: Phiên bản 3.10 trở lên (khuyên dùng Python 3.11 - 3.14).
- **Trình biên dịch C**: `gcc` (MinGW / MSYS2 trên Windows, hoặc GCC trên Linux/macOS). Kiểm tra bằng lệnh:
  ```bash
  gcc --version
  ```

### Bước 2: Cài đặt thư viện phụ thuộc
Chỉ cần cài đặt framework `flask`:
```bash
python -m pip install -r requirements.txt
```

### Bước 3: Khởi động máy chủ web
Chạy lệnh:
```bash
python app.py
```
Màn hình sẽ hiển thị thông báo:
```
🚀 Khởi động Dragon Judge Platform tại http://localhost:5000
 * Running on http://127.0.0.1:5000
```
Mở trình duyệt web của bạn và truy cập: **`http://localhost:5000`**.

---

## 📖 4. CÁCH THÊM BÀI TẬP MỚI TỪ "BÍ KÍP LUYỆN RỒNG"

Bạn có thể dễ dàng bổ sung thêm hàng trăm bài tập mới từ sách vào hệ thống bằng cách mở tệp:
`data/problems.json`

Thêm một phần tử vào mảng `"problems"` theo đúng khuôn mẫu:

```json
{
  "id": "DRAGON-09",
  "title": "Tên bài toán mới (Ví dụ: Tổng Dãy Số Tự Nhiên)",
  "chapter": "Phần I. Nhập - Xuất cơ bản",
  "difficulty": "Dễ",
  "time_limit": 1.5,
  "memory_limit": 256,
  "description": "Nhập vào số nguyên dương N. Hãy tính tổng S = 1 + 2 + ... + N.",
  "input_format": "Một số nguyên dương N (1 <= N <= 10^9).",
  "output_format": "In ra tổng S trên một dòng duy nhất.",
  "constraints": "1 <= N <= 10^9\nThời gian chạy: 1.5s",
  "sample_input": "5\n",
  "sample_output": "15\n",
  "hints": "Dùng công thức toán N * (N + 1) / 2 với kiểu dữ liệu long long để đạt độ phức tạp O(1).",
  "python_starter": "# Viết code Python 3 tại đây\nimport sys\n\ndef solve():\n    n = int(sys.stdin.read().strip())\n    print(n * (n + 1) // 2)\n\nif __name__ == '__main__':\n    solve()\n",
  "c_starter": "// Viết code C tại đây\n#include <stdio.h>\n\nint main() {\n    long long n;\n    if (scanf(\"%lld\", &n) == 1) {\n        printf(\"%lld\\n\", n * (n + 1) / 2);\n    }\n    return 0;\n}\n",
  "test_cases": [
    {
      "test_index": 1,
      "is_sample": true,
      "description": "Test cơ bản 1 (Ví dụ mẫu: 5 -> 15)",
      "input_data": "5\n",
      "expected_output": "15\n"
    },
    {
      "test_index": 2,
      "is_sample": true,
      "description": "Test cơ bản 2 (N = 3 -> 6)",
      "input_data": "3\n",
      "expected_output": "6\n"
    },
    {
      "test_index": 3,
      "is_sample": false,
      "description": "Test biên (N = 1 giá trị nhỏ nhất)",
      "input_data": "1\n",
      "expected_output": "1\n"
    },
    {
      "test_index": 4,
      "is_sample": false,
      "description": "Test trung bình (N = 1000 -> 500500)",
      "input_data": "1000\n",
      "expected_output": "500500\n"
    },
    {
      "test_index": 5,
      "is_sample": false,
      "description": "Stress test số lớn (N = 10^9 kiểm tra tràn 64-bit và O(1))",
      "input_data": "1000000000\n",
      "expected_output": "500000000500000000\n"
    }
  ]
}
```

### Cách cập nhật ngay mà không cần tắt Server:
- **Cách 1:** Truy cập trang **"Bí Kíp & Hướng Dẫn"** (`/guide`) trên web và nhấn nút **"Cập Nhật Vào Database"**.
- **Cách 2:** Gửi một yêu cầu `POST` tới endpoint:
  ```bash
  curl -X POST http://localhost:5000/api/admin/reload-problems
  ```
Hệ thống sẽ tự động đồng bộ bài tập mới và bộ 5 test cases tương ứng vào SQLite Database ngay tức thì!

---

## ⌨️ 5. CÁC PHÍM TẮT TIỆN ÍCH TRÊN GIAO DIỆN

| Phím tắt | Thao tác tương ứng |
| :--- | :--- |
| `Ctrl + Enter` | **Chạy thử code (Run Code)** với test mẫu hoặc stdin tùy chọn |
| `Ctrl + Alt + Enter` | **Nộp bài chấm điểm (Submit Code)** toàn bộ 5 test cases |
| `Ctrl + S` | Tự động lưu bản nháp vào bộ nhớ trình duyệt (LocalStorage) |

---
*Chúc các huấn luyện viên rồng luyện code vui vẻ và chinh phục trọn vẹn 303 bài tập! 🐉*
"# app-coding" 
