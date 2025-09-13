from app.context.retrieval import retrieve_policy

def handle_supplier(user_input: str):
    """Answer supplier queries using FAISS vector store."""
    context = retrieve_policy(user_input)
    return f"📄 Retrieved Policy Info:\n{context}"
