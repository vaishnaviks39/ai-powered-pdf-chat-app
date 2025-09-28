import tempfile
import os
from PIL import Image
import streamlit as st
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# LangChain imports
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.schema import HumanMessage, SystemMessage

# For PDF preview
from pdf2image import convert_from_path

# ------------------- Page Config -------------------

st.markdown(
    "<h2 style='text-align:center; margin-bottom:5px;'>🦜🔗 PDF-Chat: Interact with Multiple PDFs</h2>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; margin-top:0px; color:gray;'>Upload PDFs, preview, and chat with memory-enabled context.</p>",
    unsafe_allow_html=True
)

# Custom CSS for chat bubbles
st.markdown(
    """
    <style>
    .user-bubble {
        background-color: #DCF8C6;
        padding: 10px;
        border-radius: 10px;
        margin: 5px;
        text-align: right;
    }
    .bot-bubble {
        background-color: #E6E6E6;
        padding: 10px;
        border-radius: 10px;
        margin: 5px;
        text-align: left;
    }
    .chat-history {
        max-height: 400px;
        overflow-y: auto;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #fafafa;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------- Sidebar -------------------
st.sidebar.title("⚙️ Settings")
st.sidebar.write("Upload PDFs and configure model parameters here.")

try:
    sidebar_image = Image.open("PDF_app_banner.png")
    st.sidebar.image(sidebar_image, use_container_width=False, width=200)
except:
    pass

uploaded_files = st.sidebar.file_uploader(
    "📂 Upload one or more PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

temperature = st.sidebar.slider("🔥 Model Temperature", 0.0, 1.0, 0.1, 0.1)
top_k = st.sidebar.slider("📑 Show Top-K Relevant Passages", 1, 10, 5, 1)

# ------------------- LLM Setup -------------------
openai_api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=temperature, openai_api_key=openai_api_key)
embeddings = OpenAIEmbeddings()

# ------------------- Multi-PDF Processing -------------------
all_pages = []
temp_pdf_paths = []

if uploaded_files:
    st.subheader("Uploaded Documents Preview")
    cols = st.columns(len(uploaded_files))  # thumbnails in row
    for idx, uploaded_file in enumerate(uploaded_files):
        temp_dir = tempfile.TemporaryDirectory()
        temp_file_path = os.path.join(temp_dir.name, uploaded_file.name)
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.read())
        temp_pdf_paths.append(temp_file_path)

        # Show first page preview
        try:
            images = convert_from_path(temp_file_path, first_page=1, last_page=1)
            cols[idx].image(images[0], width=200, caption=uploaded_file.name)
        except:
            cols[idx].write(f"📄 {uploaded_file.name}")

        # Load PDF into vector DB
        loader = PyPDFLoader(temp_file_path)
        pages = loader.load_and_split()
        all_pages.extend(pages)

# ------------------- Vector Store + Direct RAG -------------------
if all_pages:
    store = Chroma.from_documents(all_pages, embeddings, collection_name="PdfDocs")

    # ------------------- Chat Interface -------------------
    st.subheader("💬 Chat with your PDFs")
    
    # Initialize chat history
    if "history" not in st.session_state:
        st.session_state["history"] = []
    
    # Chat input
    prompt = st.chat_input("Ask a question about your PDFs")

    if prompt:
        # Get relevant documents
        search_results = store.similarity_search(prompt, k=top_k)
        
        if search_results:
            # Prepare context from retrieved documents
            context = "\n\n".join([doc.page_content for doc in search_results])
            
            # Create the prompt for the LLM
            system_message = SystemMessage(content="""You are a helpful AI assistant that answers questions based on the provided PDF documents. 
            Use only the information from the context provided. If you cannot find relevant information in the context, say so clearly.
            Provide detailed and accurate answers based on the documents.""")
            
            human_message = HumanMessage(content=f"""Context from PDF documents:
{context}

Question: {prompt}

Please answer the question based on the context provided above.""")
            
            try:
                # Get response from LLM
                response_obj = llm([system_message, human_message])
                response = response_obj.content
            except Exception as e:
                response = f"Error generating response: {str(e)}"
        else:
            response = "I couldn't find any relevant information in the uploaded PDFs for your question."

        # Save to history
        st.session_state["history"].append({"user": prompt, "bot": response})

    # Display chat history
    if st.session_state["history"]:
        st.markdown("### Conversation")
        st.markdown('<div class="chat-history">', unsafe_allow_html=True)
        for chat in st.session_state["history"]:
            st.markdown(f'<div class="user-bubble">{chat["user"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="bot-bubble">{chat["bot"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------- Relevant Passages -------------------
    if prompt:
        with st.expander("🔍 Relevant Passages"):
            search = store.similarity_search_with_score(prompt, k=top_k)
            for i, (doc, score) in enumerate(search, 1):
                st.markdown(f"**Passage {i} (Score: {score:.2f})**")
                st.write(doc.page_content)
                st.markdown("---")

else:
    st.info("Please upload PDF files from the sidebar to start chatting!")