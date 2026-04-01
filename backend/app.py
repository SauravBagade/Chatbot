from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from routes.auth import router as auth_router
from routes.chat import router as chat_router
from routes.upload import router as upload_router

# -------------------------------
# 🚀 Initialize FastAPI App
# -------------------------------
app = FastAPI(
    title="LLaMA Chatbot API",
    description="ChatGPT-like chatbot using LLaMA + FastAPI",
    version="1.0.0"
)

# -------------------------------
# 🌐 CORS Configuration
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# 📌 Include Routers
# -------------------------------
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(chat_router, prefix="/api", tags=["Chat"])
app.include_router(upload_router, prefix="/api", tags=["Upload"])

# -------------------------------
# 🏠 Root Endpoint
# -------------------------------
@app.get("/")
def root():
    return {
        "status": "success",
        "message": "🚀 LLaMA Chatbot API is running"
    }

# -------------------------------
# ❤️ Health Check Endpoint
# -------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -------------------------------
# ▶️ Run App (Local Development)
# -------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
