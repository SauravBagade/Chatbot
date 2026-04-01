from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Schema
from backend.schemas import UploadResponse
from backend.model import create_vector_db
from backend.utils.security import decode_token
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
        return payload["sub"]
    except:
        raise HTTPException(status_code=403, detail="Invalid or expired token")


# -------------------------------
# 📄 Upload File Endpoint (RAG)
# -------------------------------
@router.post("/upload", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    user: str = Depends(get_current_user)
):
    try:
        # -------------------------------
        # ⚠️ File Validation
        # -------------------------------
        if not file.filename.endswith(".txt"):
            raise HTTPException(
                status_code=400,
                detail="Only .txt files are supported"
            )

        # -------------------------------
        # 📖 Read File
        # -------------------------------
        content = await file.read()

        try:
            text = content.decode("utf-8")
        except:
            raise HTTPException(
                status_code=400,
                detail="File encoding must be UTF-8"
            )

        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty"
            )

        # -------------------------------
        # ✂️ Split Large Text (Chunking)
        # -------------------------------
        chunk_size = 500
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

        # -------------------------------
        # 🧠 Create / Update Vector DB
        # -------------------------------
        create_vector_db(chunks)

        # -------------------------------
        # ✅ Response
        # -------------------------------
        return {
            "message": f"File '{file.filename}' uploaded & indexed successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
