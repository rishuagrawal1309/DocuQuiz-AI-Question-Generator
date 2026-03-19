import pdfplumber
from docx import Document


def extract_text(file_path, filename):
    
    # PDF
    if filename.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    # TXT
    elif filename.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    # DOCX
    elif filename.endswith(".docx"):
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    else:
        return None
