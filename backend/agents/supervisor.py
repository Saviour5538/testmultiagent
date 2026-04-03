import os
from .rag_summarizer import RAGAgent, SummarizerAgent
from .email_excel import EmailAgent, ExcelCheckerAgent

class Supervisor:
    def __init__(self):
        self.rag = RAGAgent()
        self.summarizer = SummarizerAgent()
        self.email = EmailAgent()
        self.excel = ExcelCheckerAgent()

    def route(self, user_input):
        user_input_lower = user_input.lower()
        if any(kw in user_input_lower for kw in ["summarize", "summary", "shorten"]):
            return "summarizer"
        elif any(kw in user_input_lower for kw in ["email", "draft", "write to"]):
            return "email"
        elif any(kw in user_input_lower for kw in ["excel", "spreadsheet", "check file", "sheet"]):
            return "excel"
        else:
            return "rag"

    def process(self, user_input, file_path=None):
        agent_type = self.route(user_input)
        
        if agent_type == "summarizer":
            # If a file was uploaded recently, summarize it. Otherwise summarize the input.
            return self.summarizer.summarize(file_path if file_path else user_input)
        elif agent_type == "email":
            return self.email.draft_email(user_input, "Drafting professional email based on request.")
        elif agent_type == "excel":
            if file_path and (file_path.endswith('.xlsx') or file_path.endswith('.xls')):
                return self.excel.check_excel(file_path)
            return "Please upload an Excel file (.xlsx or .xls) to check."
        else: # Default is RAG
            return self.rag.query(user_input)
