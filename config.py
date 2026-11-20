import os
import sys

# Base directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
TEMP_EXEC_DIR = os.path.join(BASE_DIR, "temp_exec")

# Ensure required directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(TEMP_EXEC_DIR, exist_ok=True)

# Database
DB_PATH = os.path.join(DATA_DIR, "dragon_judge.db")
PROBLEMS_JSON_PATH = os.path.join(DATA_DIR, "problems.json")

# Judge Engine Settings
DEFAULT_TIMEOUT_SECONDS = 1.5  # Base default fallback (seconds)
TIMEOUT_BY_LANGUAGE = {
    "c": 1.0,         # C is fast compiled code: 1.0s limit
    "gcc": 1.0,
    "python": 2.0,    # Python 3 is interpreted: 2.0s limit
    "python3": 2.0,
    "py": 2.0
}
MAX_OUTPUT_LENGTH = 10000      # Max characters of stdout/stderr to capture (prevents memory bomb)

# Python executable to use for sandbox execution
PYTHON_EXECUTABLE = sys.executable

# Compiler settings for C
C_COMPILER = "gcc"
C_FLAGS = ["-O2", "-std=c11", "-Wall"]

# Server settings
HOST = "0.0.0.0"
PORT = 5000
DEBUG = True
