# 🦜🔗 PDF-Chat: Interact with Multiple PDFs

A Streamlit application that lets you **upload multiple PDF documents and chat with them** using **LangChain**, **OpenAI GPT models**, and **vector embeddings (ChromaDB)**.  
You can preview PDFs, ask natural language questions, and get contextual answers grounded in the documents.  

---

## ✨ Features
- 📂 Upload and preview multiple PDFs
- 🔍 Extract text using LangChain’s PDF loader
- 📊 Store embeddings in Chroma vector database
- 💬 Ask natural language questions with context-aware answers
- 🧠 Memory-enabled conversation history
- 🎨 Beautiful Streamlit UI with chat bubbles

---

## 🛠️ Tech Stack
Python 3.10

Streamlit

LangChain

OpenAI GPT-3.5

Chroma Vector Store

Docker

Google Cloud Run (for deployment)

---

## 📦 Installation (Local)

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/pdf-chat-app.git
   cd pdf-chat-app

2. **Create and activate a virtual environment (optional):**

***For Mac***
python3 -m venv venv
source venv/bin/activate

3. **Install dependencies:**

pip install -r requirements.txt

4. **Set up environment variables by creating a .env file in the project root:**

OPENAI_API_KEY=your_openai_api_key_here

5. **Run the app:**

streamlit run chat_app.py

**Access the app at: http://localhost:8501**
