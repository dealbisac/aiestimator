import faiss
import numpy as np
from google.generativeai import embed_content
from pdf_utils import extract_text_from_pdf, chunk_text

def get_embedding(text):
    res = embed_content(model="models/embedding-001", content=text, task_type="retrieval_document")
    return np.array(res["embedding"], dtype=np.float32)

def build_faiss_index(chunks):
    dim = 768
    index = faiss.IndexFlatL2(dim)
    embeddings = [get_embedding(chunk) for chunk in chunks]
    index.add(np.vstack(embeddings))
    return index, embeddings

def load_pdf_and_build_index(path):
    text = extract_text_from_pdf(path)
    chunks = chunk_text(text)
    index, embeddings = build_faiss_index(chunks)
    return chunks, index, embeddings
