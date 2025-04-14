import PyPDF2

def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        return " ".join([p.extract_text() for p in reader.pages if p.extract_text()])

def chunk_text(text, chunk_size=1000, overlap=200):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size - overlap)]
