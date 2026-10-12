# 📚 Study Assistant RAG

A Retrieval-Augmented Generation (RAG) study assistant built entirely from scratch in Python. This tool allows users to upload university PDF notes and ask questions, receiving strictly cited answers. 

## ✨ Features

* **From-Scratch RAG Pipeline:** Custom implementation of document ingestion, chunking, embedding, retrieval, and generation.
* **Smart Chunking:** Intelligently splits text based on character count while respecting word boundaries (looking for the last space) to preserve context.
* **Strict Anti-Hallucination Guardrails:** The LLM is heavily prompted to answer *only* using the provided context and to output "I don't know" if the answer is missing.
* **Precise Citations:** Answers include strict source and page number citations mapped directly from the original PDFs.
* **Scientific Evaluation Pipeline:** Includes a custom testing script (`run_eval.py`) to measure the Top-4 Hit Rate across different chunk sizes and optimize retrieval performance.
* **Interactive UI:** Clean, user-friendly chat interface built with Streamlit.

## 📊 Performance & Evaluation

To ensure the highest retrieval accuracy, the pipeline was evaluated on a ground-truth dataset of 20 domain-specific questions. We tested the **Top-4 Hit Rate** (the percentage of queries where the correct source page was retrieved in the top 4 vector search results).

**Evaluation Results:**
* **Chunk size 800 chars (~120 words):** 100.00% Hit Rate 🏆
* **Chunk size 1500 chars (~220 words):** 95.00% Hit Rate

*Conclusion:* Empirical testing proved that smaller chunk sizes (800 characters) are significantly more effective for these academic texts. They keep the semantic vectors highly concentrated, whereas larger chunks dilute the context and cause the vector database to occasionally miss the correct paragraph.

## 🛠️ Tech Stack

* **Language:** Python 3.11+
* **PDF Processing:** PyMuPDF (`fitz`)
* **Embeddings:** `sentence-transformers` (`paraphrase-multilingual-MiniLM-L12-v2`)
* **Vector Database:** ChromaDB (Local, persistent storage)
* **LLM / Generation:** Google Gemini API (`gemini-3.8-flash`)
* **User Interface:** Streamlit
* **Package Management:** `uv`

<img width="959" height="452" alt="image" src="https://github.com/user-attachments/assets/ee82328e-4b3d-4956-922f-501bf354975c" />

