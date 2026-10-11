# 📚 Study Assistant RAG

A Retrieval-Augmented Generation (RAG) study assistant built entirely from scratch in Python. This tool allows users to upload university PDF notes and ask questions, receiving strictly cited answers. 

Designed as a portfolio project, this implementation avoids heavy frameworks like LangChain to demonstrate a deep understanding of vector databases, semantic search, prompt engineering, and RAG evaluation pipelines.

## ✨ Features

* **From-Scratch RAG Pipeline:** Custom implementation of document ingestion, chunking, embedding, retrieval, and generation.
* **Smart Chunking:** Intelligently splits text based on character count while respecting word boundaries (looking for the last space) to preserve context.
* **Strict Anti-Hallucination Guardrails:** The LLM is heavily prompted to answer *only* using the provided context and to output "I don't know" if the answer is missing.
* **Precise Citations:** Answers include strict source and page number citations mapped directly from the original PDFs.
* **Scientific Evaluation Pipeline:** Includes a custom testing script (`run_eval.py`) to measure the Top-4 Hit Rate across different chunk sizes and optimize retrieval performance.
* **Interactive UI:** Clean, user-friendly chat interface built with Streamlit.

## 🛠️ Tech Stack

* **Language:** Python 3.11+
* **PDF Processing:** PyMuPDF (`fitz`)
* **Embeddings:** `sentence-transformers` (`paraphrase-multilingual-MiniLM-L12-v2`)
* **Vector Database:** ChromaDB (Local, persistent storage)
* **LLM / Generation:** Google Gemini API (`gemini-3.8-flash`)
* **User Interface:** Streamlit
* **Package Management:** `uv`

## 📂 Project Structure

```text
study_assistant/
├── app.py                  # Main Streamlit web application
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore file
├── src/                    # Core logic modules
│   ├── ingest.py           # PDF extraction and smart chunking
│   ├── embed.py            # Vector embeddings and ChromaDB management
│   ├── retrieve.py         # Top-k semantic search
│   └── answer.py           # Prompt building and Gemini API integration
└── eval/                   # Evaluation pipeline
    ├── run_eval.py         # Automated testing for Top-4 Hit Rate
    └── questions.json      # Ground-truth dataset for evaluation
