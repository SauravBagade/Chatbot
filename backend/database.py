from pymongo import MongoClient
import os

# -------------------------------
# ⚙️ MongoDB Configuration
# -------------------------------

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

DB_NAME = "llama_chatbot"

# -------------------------------
# 🔌 Create MongoDB Client
# -------------------------------

client = MongoClient(MONGO_URL)

db = client[DB_NAME]

# -------------------------------
# 📂 Collections
# -------------------------------

users_collection = db["users"]
chat_collection = db["chats"]

# -------------------------------
# 🧪 Test Connection (Optional)
# -------------------------------

def test_connection():
    try:
        client.admin.command("ping")
        print("✅ MongoDB connected successfully")
    except Exception as e:
        print("❌ MongoDB connection failed:", e)
