# 📌 AI Quantity Estimation Assistant (PDF + Gemini + FAISS + Multilingual)

---

This notebook helps estimate quantities from uploaded engineering PDFs using:
- 📄 PDF parsing
- 🧠 Gemini Pro (via Google Generative AI SDK)
- 🗃️ FAISS vector store
- 💬 Prompt-based multilingual chat

---

## 🔧 Install Required Libraries
```python
# ✅ Clean install for compatibility
!pip uninstall -y langchain langchain-core langchain-community langchain-google-genai google-generativeai google-ai-generativelanguage -q

# ✅ Install compatible versions
!pip install -q \
  langchain==0.1.13 \
  langchain-core==0.1.45 \
  langchain-community==0.0.28 \
  langchain-google-genai==0.0.5 \
  google-generativeai==0.8.3 \
  google-ai-generativelanguage==0.6.15 \
  faiss-cpu \
  PyMuPDF \
  googletrans==4.0.0-rc1
```

---

## 🧠 Step 1: Setup Gemini Pro
```python
import google.generativeai as genai

GOOGLE_API_KEY = "your-google-api-key"  # 🔐 Replace with your actual key
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")
```

---

## 📄 Step 2: Upload & Extract PDF Text
```python
import fitz  # PyMuPDF
from google.colab import files

# Upload PDF
uploaded = files.upload()
pdf_file = next(iter(uploaded))

# Extract text
doc = fitz.open(pdf_file)
pages_text = [page.get_text() for page in doc]
full_text = "\n".join(pages_text)
print(full_text[:1000])  # Preview first 1000 chars
```

---

## 🧠 Step 3: Split & Embed Text with LangChain + FAISS
```python
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = text_splitter.split_text(full_text)
chunk_docs = [Document(page_content=c) for c in chunks]

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
faiss_index = FAISS.from_documents(chunk_docs, embedding=embeddings)
```

---

## 🌐 Step 4: Multilingual Translation Helper
```python
from googletrans import Translator
translator = Translator()

def translate_to_english(text):
    try:
        return translator.translate(text, dest='en').text
    except:
        return text
```

---

## 💬 Step 5: Define Prompt + Retrieval Chat Pipeline
```python
def generate_quantity_response(query, k=4):
    translated_query = translate_to_english(query)
    docs = faiss_index.similarity_search(translated_query, k=k)
    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
    You are a quantity surveyor assistant.
    Use the following extracted PDF context to answer the question.

    Context:
    {context}

    Question: {translated_query}

    If the answer is not in the context, say "I could not find that in the provided document."
    Be precise, factual, and respond in English.
    """

    response = model.generate_content(prompt)
    return response.text
```

---

## 🧪 Step 6: Test the System
```python
query = "Section 3 मा कति concrete लाग्छ?"
response = generate_quantity_response(query)
print(response)
```

---

## ✅ Summary
- Upload engineering drawing PDF
- Extract and chunk text
- Embed with FAISS
- Translate multilingual queries
- Retrieve context
- Ask Gemini for precise quantity estimation
