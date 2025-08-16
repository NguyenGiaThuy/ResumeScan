"""
PDF Service
Handles PDF text extraction functionality
"""
import os
import tempfile
from langchain.document_loaders import PyPDFLoader


def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text content from PDF file."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(file_content)
        tmp_pdf_path = tmp_file.name
    
    try:
        loader = PyPDFLoader(tmp_pdf_path)
        docs = loader.load()
        text_content = "\n".join([doc.page_content for doc in docs])
        return text_content
    finally:
        os.unlink(tmp_pdf_path)
