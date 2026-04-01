from datetime import datetime
from backend.database import chat_collection

# -------------------------------
# 💬 Add Message to Memory (DB)
# -------------------------------
def save_message(user_id: str, role: str, content: str):
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.utcnow()
    }

    existing_chat = chat_collection.find_one({"user_id": user_id})

    if existing_chat:
        chat_collection.update_one(
            {"user_id": user_id},
            {"$push": {"messages": message}}
        )
    else:
        chat_collection.insert_one({
            "user_id": user_id,
            "messages": [message]
        })


# -------------------------------
# 📜 Get Chat History
# -------------------------------
def get_chat_history(user_id: str):
    chat = chat_collection.find_one({"user_id": user_id})

    if not chat:
        return []

    return chat.get("messages", [])


# -------------------------------
# 🧠 Get Recent Context (for LLM)
# -------------------------------
def get_recent_context(user_id: str, limit: int = 5) -> str:
    messages = get_chat_history(user_id)

    if not messages:
        return ""

    # Take last N messages
    recent_messages = messages[-limit:]

    context = ""
    for msg in recent_messages:
        role = msg["role"]
        content = msg["content"]

        if role == "user":
            context += f"User: {content}\n"
        else:
            context += f"Assistant: {content}\n"

    return context.strip()


# -------------------------------
# 🗑️ Clear Chat History
# -------------------------------
def clear_chat_history(user_id: str):
    chat_collection.delete_one({"user_id": user_id})
