# app/main.py
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from app.summarizer import summarize_text
from app.file_utils import extract_text


app = FastAPI()

# Optional: Allow frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Smart Document Summarizer is running"}

@app.post("/summarize/")
async def summarize_file(file: UploadFile = File(...)):
    contents = await file.read()
    
    # Rewind file pointer for PDF/DOCX use
    file.file.seek(0)
    extracted_text = extract_text(file.file, file.filename)
    
    if extracted_text.startswith("Unsupported"):
        return {"error": extracted_text}
    
    summary = summarize_text(extracted_text)
    return {
        "filename": file.filename,
        "summary": summary
    }
