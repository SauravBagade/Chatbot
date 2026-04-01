import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory

# -------------------------------
# 🧠 Model Configuration
# -------------------------------
MODEL_NAME = "meta-llama/Llama-3-8b-instruct"  # change to LLaMA 4 if available

print("🔄 Loading LLaMA model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto"
)

print("✅ Model loaded successfully!")

# -------------------------------
# 🧠 Chat Memory (Temporary)
# -------------------------------
memory = ConversationBufferMemory()

# -------------------------------
# 🔍 Embedding Model
# -------------------------------
embedding_model = HuggingFaceEmbeddings()

# -------------------------------
# 📁 Vector Store Path
# -------------------------------
VECTOR_DB_PATH = "vectorstore/faiss_index"

# -------------------------------
# 📦 Load or Create Vector DB
# -------------------------------
if os.path.exists(VECTOR_DB_PATH):
    vector_db = FAISS.load_local(VECTOR_DB_PATH, embedding_model)
    print("✅ Loaded existing FAISS DB")
else:
    vector_db = None
    print("⚠️ No FAISS DB found")

# -------------------------------
# 📄 Create / Update Vector DB
# -------------------------------
def create_vector_db(texts):
    global vector_db

    if vector_db is None:
        vector_db = FAISS.from_texts(texts, embedding_model)
    else:
        vector_db.add_texts(texts)

    # Save to disk (persistent)
    vector_db.save_local(VECTOR_DB_PATH)

# -------------------------------
# 🔎 Retrieve Context (RAG)
# -------------------------------
def get_context(query):
    if vector_db is None:
        return ""

    docs = vector_db.similarity_search(query, k=3)
    return "\n".join([doc.page_content for doc in docs])

# -------------------------------
# 💬 Generate Response
# -------------------------------
def generate_response(query):
    context = get_context(query)

    prompt = f"""
You are a helpful AI assistant.

Context:
{context}

User: {query}
Assistant:
"""

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        temperature=0.7,
        top_p=0.9,
        do_sample=True
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Save memory
    memory.save_context({"input": query}, {"output": response})

    return response

# -------------------------------
# 🔄 Reset Vector DB
# -------------------------------
def reset_vector_db():
    global vector_db
    vector_db = None

    if os.path.exists(VECTOR_DB_PATH):
        import shutil
        shutil.rmtree(VECTOR_DB_PATH)
