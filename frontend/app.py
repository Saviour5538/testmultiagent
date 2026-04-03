import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
API_URL = os.environ.get("API_URL", "http://localhost:8000")

# Page Layout
st.set_page_config(
    page_title="Aakaar AI | Multi-Agent System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Light Design System (CSS)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Main App Overhaul */
    .stApp {
        background-color: #f8fafc;
        font-family: 'Inter', sans-serif;
        color: #1e293b;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }

    /* Header Styling */
    .main-header {
        background: #ffffff;
        padding: 2.5rem;
        border-radius: 24px;
        border: 1px solid #e2e8f0;
        margin-bottom: 2.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    }

    /* Chat Messages Styling */
    [data-testid="stChatMessage"] {
        background: #ffffff !important;
        border-radius: 18px !important;
        border: 1px solid #e2e8f0 !important;
        margin: 1.2rem 0 !important;
        padding: 1.5rem !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
        color: #334155 !important; /* Dark slate for readability */
    }

    [data-testid="stChatMessageUser"] {
        background: #eff6ff !important; /* Soft Blue */
        border-left: 6px solid #3b82f6 !important;
    }

    [data-testid="stChatMessageAssistant"] {
        background: #f0fdf4 !important; /* Soft Green */
        border-left: 6px solid #10b981 !important;
    }

    /* Input Field Styling */
    .stChatInputContainer {
        padding-bottom: 2rem !important;
    }

    /* Buttons & Interactions */
    .stButton>button {
        border-radius: 10px !important;
        background: #3b82f6 !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }

    .stButton>button:hover {
        background: #2563eb !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }

    /* Title Styling */
    h1 {
        font-weight: 800 !important;
        letter-spacing: -0.025em !important;
        color: #0f172a !important;
        margin-bottom: 10px !important;
    }

    /* Info card styling */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        background-color: #f1f5f9 !important;
        color: #475569 !important;
    }
</style>
""", unsafe_allow_html=True)

# Custom Header Component
st.markdown("""
<div class="main-header">
    <h1>🤖 Aakaar AI Hub</h1>
    <p style="color: #64748b; font-size: 1.1rem; margin-top: -5px;">
        Agentic swarm for RAG, Document Summarization, and Deep Analysis.
    </p>
    <div style="display: flex; gap: 0.8rem; align-items: center; margin-top: 18px;">
        <span style="background: #f0fdf4; color: #166534; padding: 4px 14px; border-radius: 20px; font-size: 0.85rem; border: 1px solid #bbf7d0; font-weight: 500;">● Online</span>
        <span style="background: #eff6ff; color: #1e40af; padding: 4px 14px; border-radius: 20px; font-size: 0.85rem; border: 1px solid #bfdbfe; font-weight: 500;">● Groq Hybrid Engine</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar for Configuration & Uploads
with st.sidebar:
    st.image("https://img.icons8.com/color/120/000000/artificial-intelligence.png", width=70)
    st.title("Control Center")
    
    with st.expander("📄 Document Library", expanded=True):
        uploaded_pdf = st.file_uploader("Upload Knowledge Source (PDF)", type="pdf")
        if uploaded_pdf:
            if st.button("🚀 Process & Ingest"):
                with st.spinner("Analyzing PDF structure..."):
                    files = {"file": uploaded_pdf}
                    response = requests.post(f"{API_URL}/ingest", files=files)
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.last_file_path = data.get("file_path")
                        st.success("Knowledge base updated!")
                    else:
                        st.error("Ingestion failed.")

    with st.expander("💹 Data Analysis", expanded=False):
        uploaded_excel = st.file_uploader("Upload Spreadsheet (XLSX)", type=["xlsx", "xls"])
        if uploaded_excel:
            if st.button("🔍 Run Validation"):
                with st.spinner("Validating data rows..."):
                    files = {"file": uploaded_excel}
                    response = requests.post(f"{API_URL}/upload-excel", files=files)
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.last_file_path = data.get("file_path")
                        st.success("Metadata extracted. Ask about it in chat!")
                    else:
                        st.error("Upload failed.")

# Main Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_file_path" not in st.session_state:
    st.session_state.last_file_path = None

# Empty State Logic
if not st.session_state.messages:
    st.info("💡 **Getting Started**: Upload a document in the sidebar to ask questions about it, or simply ask me to draft an email or summarize a topic.")

# Display Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("Message the agentic swarm..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Generating intelligence..."):
            # Call backend API
            data = {
                "message": prompt,
                "file_path": st.session_state.last_file_path
            }
            
            try:
                response = requests.post(f"{API_URL}/chat", data=data)
                if response.status_code == 200:
                    ans = response.json()["response"]
                    st.markdown(ans)
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                else:
                    st.error("Swarm connection interrupted.")
            except Exception as e:
                st.error(f"Network Error: {str(e)}")
