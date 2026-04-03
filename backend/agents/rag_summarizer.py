import os
import google.generativeai as genai
from groq import Groq
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY")) if os.getenv("GROQ_API_KEY") else None

class RAGAgent:
    def __init__(self):
        self.context = ""
        self.use_groq = groq_client is not None
        if not self.use_groq:
            try:
                self.model = genai.GenerativeModel("gemini-3.1-flash-live-preview")
            except Exception:
                self.model = genai.GenerativeModel("gemini-2.0-flash")

    def ingest(self, file_path):
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            self.context = text
            return f"Ingested {len(text)} characters from {os.path.basename(file_path)}"
        except Exception as e:
            return f"Error ingesting PDF: {str(e)}"

    def query(self, user_query):
        if not self.context:
            return "No documents ingested. Please upload a PDF first."
        
        prompt = f"""
        Context:
        {self.context[:30000]}  # Limit context for speed and safety
        
        Question: {user_query}
        
        Answer based only on the context provided. Keep it concise.
        """
        if self.use_groq:
            chat_completion = groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
            )
            return chat_completion.choices[0].message.content

        response = self.model.generate_content(prompt)
        return response.text

class SummarizerAgent:
    def __init__(self):
        self.use_groq = groq_client is not None
        if not self.use_groq:
            try:
                self.model = genai.GenerativeModel("gemini-3.1-flash-live-preview")
            except:
                self.model = genai.GenerativeModel("gemini-2.0-flash")

    def summarize(self, text_or_path):
        # If it's a file path, extract text
        text = text_or_path
        if os.path.exists(text_or_path):
            try:
                reader = PdfReader(text_or_path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
            except:
                pass

        prompt = f"Summarize the following text in a professional way:\n\n{text[:30000]}"
        if self.use_groq:
            chat_completion = groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
            )
            return chat_completion.choices[0].message.content

        response = self.model.generate_content(prompt)
        return response.text
