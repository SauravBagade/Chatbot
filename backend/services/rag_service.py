import os
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

# -------------------------------
# 🔍 Embedding Model
# -------------------------------
embedding_model = HuggingFaceEmbeddings()

# -------------------------------
# 📁 Vector DB Path
# -------------------------------
VECTOR_DB_PATH = "vectorstore/faiss_index"

# -------------------------------
# 📦 Load Vector DB (if exists)
# -------------------------------
def load_vector_db():
    if os.path.exists(VECTOR_DB_PATH):
        return FAISS.load_local(VECTOR_DB_PATH, embedding_model)
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

    chunks = split_text(text)

    if vector_db is None:
        vector_db = FAISS.from_texts(chunks, embedding_model)
    else:
        vector_db.add_texts(chunks)

    # Save to disk
    vector_db.save_local(VECTOR_DB_PATH)


# -------------------------------
# 🔎 Retrieve Relevant Context
# -------------------------------
def get_relevant_context(query: str, k: int = 3) -> str:
    if vector_db is None:
        return ""

    docs = vector_db.similarity_search(query, k=k)

    return "\n".join([doc.page_content for doc in docs])


# -------------------------------
# 🔄 Reset Vector DB
# -------------------------------
def reset_vector_db():
    global vector_db

    vector_db = None

    if os.path.exists(VECTOR_DB_PATH):
        import shutil
        shutil.rmtree(VECTOR_DB_PATH)
