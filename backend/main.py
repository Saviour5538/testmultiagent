import os
import shutil
import uvicorn
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .agents.supervisor import Supervisor
from .agents.rag_summarizer import RAGAgent

load_dotenv()

app = FastAPI(title="Multi-Agent Chatbot API")
supervisor = Supervisor()
rag = RAGAgent()

# Enable CORS for frontend storage and local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Simplified Multi-Agent API is running!"}

@app.post("/chat")
async def chat(message: str = Form(...), file_path: str = Form(None)):
    response = supervisor.process(message, file_path)
    return {"response": response}

@app.post("/ingest")
async def ingest_pdf(file: UploadFile = File(...)):
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, file.filename)
    
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    result = rag.ingest(temp_file_path)
    # Ensure supervisor case for RAG is updated
    supervisor.rag.context = rag.context
    return {"result": result, "file_path": temp_file_path}

@app.post("/upload-excel")
async def upload_excel(file: UploadFile = File(...)):
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, file.filename)
    
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {"file_path": temp_file_path}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
