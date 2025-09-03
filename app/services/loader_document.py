from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

class DocumentLoader:

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def load_pdf(self):
        try:
            loader = PyPDFLoader(self.file_path)
            docs = loader.load()
            return docs
        except FileNotFoundError as e:
            print(f"File not found: {e}")
            return []
