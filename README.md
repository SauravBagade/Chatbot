---
#chatbot
---
```

llama-chatbot/
│
├── backend/
│   ├── app.py                     # FastAPI main app
│   ├── model.py                  # LLaMA + RAG logic
│   ├── database.py               # MongoDB connection
│   ├── schemas.py                # Pydantic models
│
│   ├── routes/
│   │   ├── chat.py               # Chat endpoints (protected)
│   │   ├── upload.py             # File upload (RAG)
│   │   └── auth.py               # Login/Register API
│   │
│   ├── services/
│   │   ├── llm_service.py        # LLaMA handling
│   │   ├── rag_service.py        # FAISS vector logic
│   │   ├── memory_service.py     # Chat memory
│   │   └── auth_service.py       # Auth business logic
│   │
│   ├── utils/
│   │   ├── security.py           # JWT + password hashing
│   │   └── helpers.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── index.html                # Chat UI
│   ├── login.html                # Login page
│   ├── register.html             # Register page
│   ├── app.js                    # Chat API calls
│   ├── auth.js                   # Auth API calls
│   └── style.css
│
├── database/
│   ├── mongo-init.js             # MongoDB init script
│   └── data/                     # Persistent DB data
│
├── vectorstore/
│   └── faiss_index/              # Saved FAISS embeddings
│
├── docker/
│   ├── Dockerfile                # Backend container
│   ├── docker-compose.yml        # Backend + MongoDB
│   └── .dockerignore
│
├── .env                          # Environment variables
├── README.md
└── requirements.txt

````

---
