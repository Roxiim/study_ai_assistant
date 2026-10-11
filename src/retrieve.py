"""Top-k semantic search over the vector store."""
from src.embed import embed_texts

def retrieve(collection, question: str, k: int = 4) -> list[dict]:
    result = collection.query(query_embeddings=embed_texts([question]), n_results=k)
    hits = []
    
    if not result or not result.get("documents") or not result["documents"][0]:
        return hits
        
    for text, meta, dist in zip(result["documents"][0],
                                result["metadatas"][0],
                                result["distances"][0]):
        hits.append({
            "text": text,
            "source": meta["source"],
            "page": meta["page"],
            "score": 1 - dist,  # cosine distance -> similarity
        })
    return hits