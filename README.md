# 🦜🔗 PDF-Chat: Interact with Multiple PDFs

A Streamlit application that lets you **upload multiple PDF documents and chat with them** using **LangChain**, **OpenAI GPT models**, and **vector embeddings (ChromaDB)**.

You can preview PDFs, ask natural language questions, and get contextual answers grounded in the documents.

---

## ✨ Features

- 📂 Upload and preview multiple PDFs
- 🔍 Extract text using LangChain's PDF loader
- 📊 Store embeddings in Chroma vector database
- 💬 Ask natural language questions with context-aware answers
- 🧠 Memory-enabled conversation history
- 🎨 Beautiful Streamlit UI with chat bubbles

---

## 🛠️ Tech Stack

- **Python 3.10**
- **Streamlit**
- **LangChain**
- **OpenAI GPT-3.5**
- **Chroma Vector Store**
- **Docker**
- **Google Cloud Run** (for deployment)

---

## 📦 Installation (Local)

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/pdf-chat-app.git
cd pdf-chat-app
```

### 2. Create and activate a virtual environment (optional)

**For Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**For Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Run the app
```bash
streamlit run chat_app.py
```

**Access the app at:** http://localhost:8501

---

## 🐳 Docker Installation

### Build and run with Docker
```bash
docker build -t pdf-chat-app .
docker run -p 8501:8501 --env-file .env pdf-chat-app
```

---

## ☁️ Deployment

### Google Cloud Run
1. Build and push the Docker image to Google Container Registry
2. Deploy to Cloud Run with environment variables set
3. Access your deployed application

---

## 🚀 Usage

1. **Upload PDFs**: Use the sidebar to upload one or more PDF files
2. **Preview**: View uploaded PDFs in the preview section
3. **Ask Questions**: Type your questions in the chat interface
4. **Get Answers**: Receive contextual answers based on your documents
5. **Chat History**: View conversation history with memory

---
