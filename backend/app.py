from fastapi import FastAPI, UploadFile, File
from backend.question_generator import generate_questions, generate_mcqs
from backend.text_extractor import extract_text
import os
import shutil

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

        # Extract text 
        extracted_text = extract_text(file_location, file.filename)

        if not extracted_text:
             os.remove(file_location)  # cleanup
             return {"error": "Could not extract text from file"}

	
        # Generate questions
        questions = generate_questions(extracted_text)
        mcqs = generate_mcqs(extracted_text)

        # Delete temp file
        os.remove(file_location)

        return {
            "filename": file.filename,
            "questions": questions,
            "mcqs": mcqs
        }

    except Exception as e:
        return {
            "error": str(e)
        }
