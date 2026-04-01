import os
import shutil

# ✅ UPDATED IMPORTS
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# -------------------------------
# 🔍 Embedding Model
# -------------------------------
embedding_model = HuggingFaceEmbeddings()

# -------------------------------
# 📁 Vector DB Path
# -------------------------------
VECTOR_DB_PATH = "vectorstore/faiss_index"

# Ensure directory exists
os.makedirs(VECTOR_DB_PATH, exist_ok=True)

# -------------------------------
# 📦 Load Vector DB (if exists)
# -------------------------------
def load_vector_db():
    try:
        if os.path.exists(os.path.join(VECTOR_DB_PATH, "index.faiss")):
            return FAISS.load_local(VECTOR_DB_PATH, embedding_model)
    except Exception as e:
        print("❌ Load vector DB error:", e)

    return None


vector_db = load_vector_db()


# -------------------------------
# ✂️ Text Chunking
# -------------------------------
def split_text(text: str, chunk_size: int = 500):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


# -------------------------------
# 📄 Create / Update Vector DB
# -------------------------------
def create_or_update_vector_db(text: str):
    global vector_db

    try:
        chunks = split_text(text)

        if vector_db is None:
            vector_db = FAISS.from_texts(chunks, embedding_model)
        else:
            vector_db.add_texts(chunks)

        # Save to disk
        vector_db.save_local(VECTOR_DB_PATH)

    except Exception as e:
        print("❌ Vector DB error:", e)


# -------------------------------
# 🔎 Retrieve Relevant Context
# -------------------------------
def get_relevant_context(query: str, k: int = 3) -> str:
    try:
        if vector_db is None:
            return ""

        docs = vector_db.similarity_search(query, k=k)

        return "\n".join([doc.page_content for doc in docs])

    except Exception as e:
        print("❌ Retrieval error:", e)
        return ""


# -------------------------------
# 🔄 Reset Vector DB
# -------------------------------
def reset_vector_db():
    global vector_db

    try:
        vector_db = None

        if os.path.exists(VECTOR_DB_PATH):
            shutil.rmtree(VECTOR_DB_PATH)

        os.makedirs(VECTOR_DB_PATH, exist_ok=True)

    except Exception as e:
        print("❌ Reset error:", e)
