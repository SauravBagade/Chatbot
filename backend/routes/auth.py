from fastapi import APIRouter, HTTPException
from datetime import datetime

# Schemas
from schemas import UserRegister, UserLogin, TokenResponse

# Security
from utils.security import hash_password, verify_password, create_access_token

# Database
from database import users_collection

# -------------------------------
# 🚀 Router Setup
# -------------------------------
router = APIRouter()


# -------------------------------
# 🆕 Register User
# -------------------------------
@router.post("/register")
def register(user: UserRegister):
    try:
        # Check if user already exists
        existing_user = users_collection.find_one({"username": user.username})
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        # Hash password
        hashed_password = hash_password(user.password)

        # Save user
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

        # Create JWT token
        token = create_access_token({"sub": user.username})

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------
# 👤 Get Current User (Optional)
# -------------------------------
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils.security import decode_token

security = HTTPBearer()

@router.get("/me")
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = decode_token(credentials.credentials)
        return {"username": payload["sub"]}
    except:
        raise HTTPException(status_code=403, detail="Invalid token")
