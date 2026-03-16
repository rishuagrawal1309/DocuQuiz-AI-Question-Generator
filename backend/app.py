from fastapi import FastAPI, UploadFile, File
import shutil
from backend.text_extractor import extract_text_from_pdf

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "DocuQuiz AI API is running"}

@app.get("/health")
def health_check():
    return {"status": "OK"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    file_location = f"temp_{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text_from_pdf(file_location)

    return {
        "filename": file.filename,
        "extracted_text": extracted_text[:500]  # show first 500 chars
    }
