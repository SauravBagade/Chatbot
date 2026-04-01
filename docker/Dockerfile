# -------------------------------
# 🐳 Base Image
# -------------------------------
FROM python:3.10-slim

# -------------------------------
# ⚙️ Environment
# -------------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# -------------------------------
# 📁 Working Directory
# -------------------------------
WORKDIR /app

# -------------------------------
# 📦 System Dependencies
# -------------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------
# 📄 Copy Requirements
# -------------------------------
COPY backend/requirements.txt .

# -------------------------------
# 📥 Install Dependencies
# -------------------------------
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# -------------------------------
# 📂 Copy Project Files
# -------------------------------
COPY backend ./backend
COPY vectorstore ./vectorstore

# -------------------------------
# 🌐 Expose Port
# -------------------------------
EXPOSE 8000

# -------------------------------
# 🚀 Run App
# -------------------------------
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
