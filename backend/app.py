from fastapi import FastAPI, UploadFile, File
from backend.question_generator import generate_questions
from backend.text_extractor import extract_text_from_pdf
import os
import shutil

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "DocuQuiz AI API is running"}


@app.get("/health")
def health_check():
    return {"status": "OK"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_location = f"temp_{file.filename}"

        # Save uploaded file
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract text from PDF
        extracted_text = extract_text_from_pdf(file_location)

        # Generate questions
        questions = generate_questions(extracted_text)

        # Delete temp file
        os.remove(file_location)

        return {
            "filename": file.filename,
            "questions": questions
        }

    except Exception as e:
        return {
            "error": str(e)
        }
