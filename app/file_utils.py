# app/file_utils.py
import PyPDF2
import docx
import os

def extract_text_from_pdf(file) -> str:
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file) -> str:
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text(file, filename: str) -> str:
    extension = os.path.splitext(filename)[1].lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file)
    elif extension == ".docx":
        return extract_text_from_docx(file)
    elif extension == ".txt":
        return file.read().decode("utf-8")
    else:
        return "Unsupported file type"
