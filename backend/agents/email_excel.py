import os
import google.generativeai as genai
from groq import Groq
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY")) if os.getenv("GROQ_API_KEY") else None

class EmailAgent:
    def __init__(self):
        self.use_groq = groq_client is not None
        if not self.use_groq:
            try:
                self.model = genai.GenerativeModel("gemini-3.1-flash-live-preview")
            except:
                self.model = genai.GenerativeModel("gemini-2.0-flash")

    def draft_email(self, user_input, context=""):
        prompt = f"""
        Context: {context}
        User Request: {user_input}
        
        Write a professional email based on the request and context above.
        """
        if self.use_groq:
            chat_completion = groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
            )
            return chat_completion.choices[0].message.content

        response = self.model.generate_content(prompt)
        return response.text

class ExcelCheckerAgent:
    def __init__(self):
        self.use_groq = groq_client is not None
        if not self.use_groq:
            try:
                self.model = genai.GenerativeModel("gemini-3.1-flash-live-preview")
            except:
                self.model = genai.GenerativeModel("gemini-2.0-flash")

    def check_excel(self, file_path):
        try:
            df = pd.read_excel(file_path)
            # Basic analysis
            columns = df.columns.tolist()
            num_rows = len(df)
            summary = f"Valid Excel file with {num_rows} rows and columns: {', '.join(columns)}"
            
            # Simple validation check with Gemini
            prompt = f"Analyze the structure of this Excel file. Columns: {columns}. Is this structure valid for a standard business report? Why or why not?"
            if self.use_groq:
                chat_completion = groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile",
                )
                response_text = chat_completion.choices[0].message.content
            else:
                response = self.model.generate_content(prompt)
                response_text = response.text
            
            return f"{summary}\n\nAnalysis:\n{response_text}"
        except Exception as e:
            return f"Error checking Excel: {str(e)}"
