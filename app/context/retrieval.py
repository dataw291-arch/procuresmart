import os
import pickle
import faiss
import numpy as np
from openai import OpenAI

client = OpenAI()

VECTOR_DIR = "data/vector_store"
INDEX_FILE = os.path.join(VECTOR_DIR, "faiss_index.bin")
META_FILE = os.path.join(VECTOR_DIR, "metadata.pkl")

def embed_text(texts):
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=texts
    )
    return [r.embedding for r in response.data]

def retrieve_policy(query: str, top_k=3) -> str:
    """Retrieve supplier policy chunks from FAISS."""
    if not os.path.exists(INDEX_FILE) or not os.path.exists(META_FILE):
        return "⚠️ Vector index not built. Run scripts/build_vectorstore.py first."

    index = faiss.read_index(INDEX_FILE)
    with open(META_FILE, "rb") as f:
        docs = pickle.load(f)

    q_emb = embed_text([query])
    D, I = index.search(np.array(q_emb).astype("float32"), top_k)

    results = []
    for idx in I[0]:
        if 0 <= idx < len(docs):
            results.append(f"[Source: {docs[idx]['source']}]\n{docs[idx]['content']}")
    return "\n\n".join(results)
