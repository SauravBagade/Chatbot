from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# -------------------------------
# 🔐 Auth Schemas
# -------------------------------

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# -------------------------------
# 💬 Chat Schemas
# -------------------------------

class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    response: str


class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[datetime] = None


class ChatHistory(BaseModel):
    user_id: str
    messages: List[Message]


# -------------------------------
# 📄 Upload Schemas
# -------------------------------

class UploadResponse(BaseModel):
    message: str


# -------------------------------
# 🗄️ Database Schemas (Optional)
# -------------------------------

class UserInDB(BaseModel):
    username: str
    password: str  # hashed password


class ChatInDB(BaseModel):
    user_id: str
    messages: List[Message]
