import chromadb
from sklearn.feature_extraction.text import HashingVectorizer

_vectorizer = HashingVectorizer(n_features=256, alternate_sign=False, norm="l2")

def embed(texts):
    return _vectorizer.transform(texts).toarray().tolist()

def get_collection():
    client = chromadb.PersistentClient(path="./chroma_db")
    return client.get_or_create_collection("company_docs", metadata={"hnsw:space": "cosine"})

def build_prompt(question, chunks):
    context = "\n".join(f"- {c}" for c in chunks)
    return (
        "You are a helpful company assistant. Answer using the context below.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\nAnswer:"
    )
