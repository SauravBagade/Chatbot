// -------------------------------
// 🚀 MongoDB Initialization Script
// -------------------------------

// Create database
db = db.getSiblingDB("llama_chatbot");

// -------------------------------
// 👤 Create Users Collection
// -------------------------------
db.createCollection("users");

// Create index (unique username)
db.users.createIndex({ username: 1 }, { unique: true });

// -------------------------------
// 💬 Create Chat Collection
// -------------------------------
db.createCollection("chats");

// Index for faster queries
db.chats.createIndex({ user_id: 1 });

// -------------------------------
// 🧪 Insert Test User (Optional)
// -------------------------------
db.users.insertOne({
  username: "testuser",
  password: "$2b$12$examplehashedpassword", // replace later
  created_at: new Date()
});

print("✅ MongoDB initialized successfully");
