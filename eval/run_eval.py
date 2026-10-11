import json
import os
from src.ingest import chunk_pdf
from src.embed import get_collection, add_chunks
from src.answer import answer

def evaluate_chunk_size(chunk_size: int, overlap: int) -> float:
    """
    Creates an isolated vector database for the given chunk size,
    runs all questions from the test set, and calculates the Top-4 Hit Rate.
    """
    eval_db_path = f"eval_db_{chunk_size}"
    
    print(f"\n{'='*40}")
    print(f"Evaluating Chunk Size: {chunk_size} characters")
    print(f"{'='*40}")
    
    # 1. Initialize isolated collection for this specific chunk size
    collection = get_collection(name="eval_notes", persist_dir=eval_db_path)
    
    # Check if we already populated it (simple check: count > 0)
    if collection.count() == 0:
        print(f"Creating database for size {chunk_size}...")
        # Assuming Lab9_EN.pdf is your test document in data/
        pdf_path = os.path.join("data", "Lab9_EN.pdf")
        if os.path.exists(pdf_path):
            chunks = chunk_pdf(pdf_path, size=chunk_size, overlap=overlap)
            add_chunks(collection, chunks)
        else:
            print(f"Warning: {pdf_path} not found. Please ensure it is in the data folder.")
    else:
        print(f"Database for size {chunk_size} already exists.")
        
    # 2. Load the evaluation questions
    try:
        with open(os.path.join("eval", "questions.json"), "r", encoding="utf-8") as f:
            questions = json.load(f)
    except FileNotFoundError:
        print("eval/questions.json not found! Please create it with test questions.")
        return 0.0
        
    hits = 0
    total = len(questions)
    
    print("\nRunning test questions...")
    # 3. Evaluate Top-4 Hit Rate
    for q in questions:
        query = q["question"]
        expected_source = q["expected_source"]
        expected_page = q["expected_page"]
        
        # Retrieve the top 4 contexts for the current question
        # answer() returns (generated_text, retrieved_passages)
        _, retrieved_passages = answer(collection, query, k=4)
        
        # Check if the expected document and page are in our top 4 results
        match_found = any(
            res["source"] == expected_source and res["page"] == expected_page
            for res in retrieved_passages
        )
                
        if match_found:
            hits += 1
            print(f"✅ HIT: '{query}'")
        else:
            print(f"❌ MISS: '{query}' (Expected: {expected_source} Page: {expected_page})")
            
    hit_rate = (hits / total) * 100 if total > 0 else 0
    print(f"\nResult for chunk size {chunk_size}: {hit_rate:.2f}% Hit Rate ({hits}/{total} matches)")
    return hit_rate

if __name__ == "__main__":
    print("Starting RAG Pipeline Evaluation...")
    
    # Test with 800 characters (~120 words)
    rate_800 = evaluate_chunk_size(chunk_size=800, overlap=100)
    
    # Test with 1500 characters (~220 words)
    rate_1500 = evaluate_chunk_size(chunk_size=1500, overlap=200)
    
    # Final Report
    print("\n" + "#"*40)
    print("FINAL COMPARISON REPORT")
    print("#"*40)
    print(f"Chunk size 800 chars : {rate_800:.2f}% Hit Rate")
    print(f"Chunk size 1500 chars: {rate_1500:.2f}% Hit Rate")