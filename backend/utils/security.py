from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# -------------------------------
# 🔐 JWT Configuration
# -------------------------------
SECRET_KEY = "supersecretkey"  # change in production (.env)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 2

# -------------------------------
# 🔑 Password Hashing (bcrypt)
# -------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# -------------------------------
# 🪪 Create JWT Token
# -------------------------------
def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# -------------------------------
# 🔍 Decode JWT Token
# -------------------------------
def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid or expired token")


# -------------------------------
# 👤 Get Current User (Dependency)
# -------------------------------
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    token = credentials.credentials

    payload = decode_token(token)

    username = payload.get("sub")

    if not username:
        raise HTTPException(status_code=403, detail="Invalid token payload")

    return username
