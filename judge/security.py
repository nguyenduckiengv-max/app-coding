import ast
import re

FORBIDDEN_PYTHON_MODULES = {
    "os", "subprocess", "socket", "shutil", "pty", "commands",
    "ctypes", "winreg", "pickle", "urllib", "requests", "http", "ftplib",
    "smtplib", "telnetlib", "webbrowser", "pathlib", "glob"
}

FORBIDDEN_PYTHON_CALLS = {
    "eval", "exec", "__import__", "compile", "open"
}

FORBIDDEN_C_HEADERS = [
    r"<windows\.h>", r"<winsock\.h>", r"<winsock2\.h>", r"<unistd\.h>",
    r"<sys/socket\.h>", r"<netinet/in\.h>", r"<arpa/inet\.h>",
    r"<process\.h>", r"<direct\.h>", r"<io\.h>"
]

FORBIDDEN_C_FUNCTIONS = [
    r"\bsystem\s*\(", r"\bpopen\s*\(", r"\bfork\s*\(",
    r"\bexec[a-z]*\s*\(", r"\bCreateProcess[a-zA-Z]*\s*\(",
    r"\bremove\s*\(", r"\bunlink\s*\(", r"\brename\s*\("
]


def check_python_safety(code: str):
    """
    Kiem tra an toan ma nguon Python bang cach phan tich AST.
    Chan cac thu vien va ham he thong nguy hiem.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        # Neu cu phap sai, de trinh thong dich Python xu ly thanh CE/RTE
        return True, ""

    for node in ast.walk(tree):
        # Kiem tra import ...
        if isinstance(node, ast.Import):
            for alias in node.names:
                mod = alias.name.split('.')[0]
                if mod in FORBIDDEN_PYTHON_MODULES:
                    return False, f"Bảo mật: Không được phép import thư viện hệ thống '{mod}'."
        
        # Kiem tra from ... import ...
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                mod = node.module.split('.')[0]
                if mod in FORBIDDEN_PYTHON_MODULES:
                    return False, f"Bảo mật: Không được phép import từ thư viện '{mod}'."
        
        # Kiem tra goi ham nguy hiem
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
                if func_name in FORBIDDEN_PYTHON_CALLS:
                    return False, f"Bảo mật: Không được phép gọi hàm '{func_name}'."
            elif isinstance(node.func, ast.Attribute):
                # Chan cac thuoc tinh he thong nguy hiem nhu __subclasses__, __globals__
                attr_name = node.func.attr
                if attr_name in ("__subclasses__", "__globals__", "__builtins__"):
                    return False, f"Bảo mật: Không được phép truy cập thuộc tính nhạy cảm '{attr_name}'."

    return True, ""


def check_c_safety(code: str):
    """
    Kiem tra an toan ma nguon C bang regex.
    Chan cac header va ham goi lenh he thong / network.
    """
    # Kiem tra header bi cam
    for pattern in FORBIDDEN_C_HEADERS:
        if re.search(pattern, code, re.IGNORECASE):
            return False, f"Bảo mật: Không được phép bao hàm thư viện hệ thống bị giới hạn ({pattern.replace('\\', '')})."

    # Kiem tra ham bi cam
    for pattern in FORBIDDEN_C_FUNCTIONS:
        if re.search(pattern, code):
            return False, f"Bảo mật: Không được phép gọi hàm thực thi hệ thống hoặc can thiệp tệp tin ({pattern.replace('\\', '')})."

    return True, ""


def check_code_safety(code: str, language: str):
    """
    Ham tong quat kiem tra ma nguon theo ngon ngu duoc chon.
    """
    lang = language.lower().strip()
    if lang in ("python", "python3", "py"):
        return check_python_safety(code)
    elif lang in ("c", "gcc"):
        return check_c_safety(code)
    else:
        return False, f"Ngôn ngữ '{language}' hiện chưa được hỗ trợ."
