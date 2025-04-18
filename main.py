from embedder import load_pdf_and_build_index
from translator import detect_language, translate_text
from prompt_utils import generate_answer
from pdf_utils import extract_text_from_pdf

def process_query(pdf_path, query):
    # Load chunks and FAISS
    chunks, index, embeddings = load_pdf_and_build_index(pdf_path)

    # Translate query to English
    lang = detect_language(query)
    en_query = translate_text(query, "en") if lang != "en" else query

    # Get answer
    answer = generate_answer(en_query, chunks, index)

    # Translate back to user's language
    return translate_text(answer, lang) if lang != "en" else answer

if __name__ == "__main__":
    path = "datsets/Estimating-Costing-civil.pdf"
    while True:
        q = input("Ask a quantity estimation question (or type 'exit'): ")
        if q.lower() == "exit":
            break
        print(process_query(path, q))
