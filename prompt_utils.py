from google.generativeai import GenerativeModel

model = GenerativeModel("gemini-1.5-flash-latest")

def generate_answer(query, chunks, index, top_k=3):
    from embedder import get_embedding
    query_emb = get_embedding(query).reshape(1, -1)
    _, indices = index.search(query_emb, top_k)
    relevant = [chunks[i] for i in indices[0]]

    prompt = "You are an expert Quantity Estimation Assistant. Use the context:\n"
    for i, chunk in enumerate(relevant):
        prompt += f"[{i+1}] {chunk}\n\n"
    prompt += f"User asked: {query}\nGive your estimation or answer clearly:\n"

    return model.generate_content(prompt).text
