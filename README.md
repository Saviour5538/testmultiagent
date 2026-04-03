# 🚀 Aakaar AI Agentic System

A high-performance, multi-agent AI system designed for advanced RAG, text summarization, email drafting, and Excel validation. Powered by **Groq** (primary) and **Google Gemini** (fallback).

---

## 🏗️ System Architecture

The project follows a **Supervisor-Agent pattern**:
- **Supervisor Agent**: The "brain" that routes user requests to the appropriate specialized agent based on natural language intent.
- **RAG Agent**: Handles PDF ingestion and context-aware retrieval-augmented generation.
- **Summarization Agent**: Provides concise summaries of long documents or text snippets.
- **Email Agent**: Drafts professional emails based on context and user instructions.
- **Excel Checker Agent**: Validates spreadsheet structure for business report compatibility.

---

## ⚡ Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: Streamlit (Premium UI with Glassmorphism)
- **LLM Engine**: Groq SDK (`llama-3.1-70b-versatile`)
- **Fallback**: Google Generative AI (`gemini-1.5-flash`)
- **Deployment**: Render-ready with dedicated `Procfile`

---

## 🛠️ Setup & Installation

### 1. Prerequisite Keys
You will need API keys from:
1. [Groq Cloud](https://console.groq.com/)
2. [Google AI Studio](https://aistudio.google.com/)

### 2. Local Installation
```bash
# Clone the repository
git clone https://github.com/Saviour5538/testmultiagent.git
cd testmultiagent

# Install dependencies
pip install -r requirements.txt

# Configure Environment
cp env.template .env
# Edit .env and paste your API keys
```

### 3. Running Locally
```bash
# Start the Backend (FastAPI)
python -m backend.main

# Start the Frontend (Streamlit)
streamlit run frontend/app.py
```

---

## 📂 API Reference (For Platforms & Testing)

The system provides a unified gateway for agent interaction.

### Unified Agent Chat
- **Endpoint**: `POST /chat`
- **Method**: `POST`
- **Body (Form Data)**:
    - `message`: (string) Your task or query.
    - `file_path`: (string, optional) Path to an ingested PDF or Excel file.

### Knowledge Ingestion
- **Endpoint**: `POST /ingest`
- **Method**: `POST`
- **Body (File)**: `file` (PDF binary)
- **Returns**: `file_path` for use in context-aware chats.

### Excel Validation
- **Endpoint**: `POST /upload-excel`
- **Method**: `POST`
- **Body (File)**: `file` (Excel binary)

---

## ☁️ Deployment

This project is optimized for **Render**.

1. **New Web Service**: Connect your GitHub repo.
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `python -m backend.main`
4. **Environment Variables**:
   - `GOOGLE_API_KEY`: [Your Key]
   - `GROQ_API_KEY`: [Your Key]
   - `PYTHONPATH`: `.`

---

## 🔒 Security
Sensitive files such as `.env` and `__pycache__` are strictly excluded via `.gitignore`. An `env.template` is provided for safe configuration reference.
