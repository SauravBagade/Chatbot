from datetime import datetime

# Security
from utils.security import hash_password, verify_password, create_access_token

# Database
from database import users_collection


# -------------------------------
# 🆕 Register User
# -------------------------------
def register_user(username: str, password: str):
    # Check if user already exists
    existing_user = users_collection.find_one({"username": username})

    if existing_user:
        return None

    # Hash password
    hashed_password = hash_password(password)

    # Save user in DB
    users_collection.insert_one({
        "username": username,
        "password": hashed_password,
        "created_at": datetime.utcnow()
    })

    return True


# -------------------------------
# 🔐 Login User
# -------------------------------
def login_user(username: str, password: str):
    db_user = users_collection.find_one({"username": username})

    if not db_user:
        return None

    # Verify password
    if not verify_password(password, db_user["password"]):
        return None

    # Create JWT token
    token = create_access_token({"sub": username})

    return token


# -------------------------------
# 👤 Get User (Optional Helper)
# -------------------------------
def get_user(username: str):
    return users_collection.find_one({"username": username})
