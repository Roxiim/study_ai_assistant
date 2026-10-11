"""Embeddings (sentence-transformers) and the vector store (ChromaDB)."""
import chromadb
from sentence_transformers import SentenceTransformer

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
_model = None

def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        print("Loading embedding model...")
        _model = SentenceTransformer(MODEL_NAME)
    return _model

def embed_texts(texts: list[str]) -> list[list[float]]:
    return _get_model().encode(texts, normalize_embeddings=True).tolist()

def get_collection(name: str = "notes", persist_dir: str = "chroma_db", reset: bool = False):
    client = chromadb.PersistentClient(path=persist_dir)
    if reset:
        try:
            client.delete_collection(name)
        except Exception:
            pass  
            
    return client.get_or_create_collection(
        name=name, metadata={"hnsw:space": "cosine"}
    )

def add_chunks(collection, chunks: list[dict], batch_size: int = 64) -> None:
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        texts = [c["text"] for c in batch]
        
        collection.upsert(
            ids=[c["id"] for c in batch],
            documents=texts,
            embeddings=embed_texts(texts),
            metadatas=[{"source": c["source"], "page": c["page"]} for c in batch],
        )