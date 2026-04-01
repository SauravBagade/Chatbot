from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# ✅ FIXED IMPORTS
from backend.schemas import UserRegister, UserLogin, TokenResponse
from backend.database import users_collection
from backend.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token
)

# -------------------------------
# 🚀 Router Setup
# -------------------------------
router = APIRouter()
security = HTTPBearer()


# -------------------------------
# 🆕 Register User
# -------------------------------
@router.post("/register")
def register(user: UserRegister):
    try:
        existing_user = users_collection.find_one({"username": user.username})

        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        hashed_password = hash_password(user.password)

        users_collection.insert_one({
            "username": user.username,
            "password": hashed_password,
            "created_at": datetime.utcnow()
        })

        return {"message": "User registered successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------
# 🔐 Login User
# -------------------------------
@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin):
    try:
        db_user = users_collection.find_one({"username": user.username})

        if not db_user:
            raise HTTPException(status_code=400, detail="User not found")

        if not verify_password(user.password, db_user["password"]):
            raise HTTPException(status_code=400, detail="Invalid password")

        token = create_access_token({"sub": user.username})

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------
# 👤 Get Current User
# -------------------------------
@router.get("/me")
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = decode_token(credentials.credentials)
        return {"username": payload["sub"]}
    except:
        raise HTTPException(status_code=403, detail="Invalid token")
