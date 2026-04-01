from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime

# Schemas
from backend.schemas import ChatRequest, ChatResponse, Message
from backend.model import generate_response
from backend.utils.security import decode_token
from backend.database import chat_collection
# -------------------------------
# 🚀 Router Setup
# -------------------------------
router = APIRouter()
security = HTTPBearer()


# -------------------------------
# 🔐 Get Current User (JWT)
# -------------------------------
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = decode_token(credentials.credentials)
        return payload["sub"]  # username
    except:
        raise HTTPException(status_code=403, detail="Invalid or expired token")


# -------------------------------
# 💬 Chat Endpoint
# -------------------------------
@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, user: str = Depends(get_current_user)):
    try:
        user_query = request.query.strip()

        if not user_query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        # 🔹 Generate response from LLaMA
        bot_response = generate_response(user_query)

        # -------------------------------
        # 🗄️ Save Chat in MongoDB
        # -------------------------------
        user_chat = chat_collection.find_one({"user_id": user})

        user_message = {
            "role": "user",
            "content": user_query,
            "timestamp": datetime.utcnow()
        }

        bot_message = {
            "role": "assistant",
            "content": bot_response,
            "timestamp": datetime.utcnow()
        }

        if user_chat:
            chat_collection.update_one(
                {"user_id": user},
                {
                    "$push": {
                        "messages": {
                            "$each": [user_message, bot_message]
                        }
                    }
                }
            )
        else:
            chat_collection.insert_one({
                "user_id": user,
                "messages": [user_message, bot_message]
            })

        return {"response": bot_response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------
# 📜 Get Chat History
# -------------------------------
@router.get("/history")
def get_chat_history(user: str = Depends(get_current_user)):
    chat = chat_collection.find_one({"user_id": user})

    if not chat:
        return {"messages": []}

    return {"messages": chat.get("messages", [])}


# -------------------------------
# 🗑️ Clear Chat History
# -------------------------------
@router.delete("/history")
def clear_chat_history(user: str = Depends(get_current_user)):
    chat_collection.delete_one({"user_id": user})
    return {"message": "Chat history cleared"}
