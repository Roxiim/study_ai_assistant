"""Prompt building, LLM generation, and the final answer."""
import os
import google.generativeai as genai
from dotenv import load_dotenv
from src.retrieve import retrieve

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Please check your .env file.")

genai.configure(api_key=api_key)
_llm_model = genai.GenerativeModel('gemini-3.8-flash')

PROMPT_TEMPLATE = """You are a study assistant. Answer the question using ONLY the \
context below. Each context passage is labeled with its source file and page.

Rules:
- If the context does not contain the answer, reply exactly: "I don't know based on the provided documents."
- Do not use outside knowledge and do not guess.
- Cite the sources you used at the end, as (file, page).
- Answer in the same language as the question.

Context:
{context}

Question: {question}

Answer:"""

def generate(prompt: str) -> str:
    """Call the Gemini API with the generated prompt."""
    response = _llm_model.generate_content(prompt)
    return response.text

def build_prompt(question: str, hits: list[dict]) -> str:
    context = "\n\n".join(
        f"[{h['source']}, page {h['page']}]\n{h['text']}" for h in hits
    )
    return PROMPT_TEMPLATE.format(context=context, question=question)

def answer(collection, question: str, k: int = 4) -> tuple[str, list[dict]]:
    """Return (answer_text, retrieved_passages)."""
    hits = retrieve(collection, question, k)
    if not hits:
        return "I don't know based on the provided documents.", []
        
    return generate(build_prompt(question, hits)), hits

if __name__ == "__main__":
    from src.embed import get_collection
    
    print("Testing the pipeline...")
    col = get_collection()
    test_question = "What is a projection transformation?"
    ans, passages = answer(col, test_question)
    
    print(f"\nQuestion: {test_question}")
    print(f"\nAnswer:\n{ans}")