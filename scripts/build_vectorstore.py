import os
import pickle
import faiss
import numpy as np
from PyPDF2 import PdfReader
from openai import OpenAI

client = OpenAI()

DATA_DIR = "data"
VECTOR_DIR = "data/vector_store"
INDEX_FILE = os.path.join(VECTOR_DIR, "faiss_index.bin")
META_FILE = os.path.join(VECTOR_DIR, "metadata.pkl")

def embed_text(texts):
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=texts
    )
    return [r.embedding for r in response.data]

def load_pdfs():
    docs = []
    for file in os.listdir(DATA_DIR):
        if file.endswith(".pdf"):
            path = os.path.join(DATA_DIR, file)
            reader = PdfReader(path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            chunks = [text[i:i+500] for i in range(0, len(text), 500)]
            for chunk in chunks:
                docs.append({"source": file, "content": chunk})
    return docs

def build_index():
    docs = load_pdfs()
    texts = [d["content"] for d in docs]
    embeddings = embed_text(texts)

    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))

    os.makedirs(VECTOR_DIR, exist_ok=True)
    faiss.write_index(index, INDEX_FILE)
    with open(META_FILE, "wb") as f:
        pickle.dump(docs, f)

    print(f"✅ Built FAISS index with {len(docs)} chunks.")

if __name__ == "__main__":
    build_index()
