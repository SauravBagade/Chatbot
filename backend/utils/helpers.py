import os
from datetime import datetime


# -------------------------------
# 🕒 Get Current UTC Time
# -------------------------------
def get_current_time():
    return datetime.utcnow()


# -------------------------------
# 🧹 Clean Text (Basic)
# -------------------------------
def clean_text(text: str) -> str:
    if not text:
        return ""

    return text.strip()


# -------------------------------
# ✂️ Split Text into Chunks
# -------------------------------
def split_text(text: str, chunk_size: int = 500):
    if not text:
        return []

    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


# -------------------------------
# 📁 Ensure Directory Exists
# -------------------------------
def ensure_directory(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


# -------------------------------
# 📄 Validate File Type
# -------------------------------
def is_valid_txt_file(filename: str) -> bool:
    return filename.endswith(".txt")


# -------------------------------
# 🔡 Safe Decode File Content
# -------------------------------
def decode_file(content: bytes) -> str:
    try:
        return content.decode("utf-8")
    except:
        raise ValueError("File must be UTF-8 encoded")


# -------------------------------
# 📏 Limit Text Length (Optional)
# -------------------------------
def limit_text_length(text: str, max_length: int = 2000) -> str:
    return text[:max_length]
