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


##🚀 Installation & Setup

1. Clone the repository
Bash
git clone [https://github.com/your-username/rag-study-assistant.git](https://github.com/your-username/rag-study-assistant.git)
cd rag-study-assistant
2. Create and activate a virtual environment
Using uv (Recommended):

Bash
uv venv
# Windows:
.\.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
(If you use standard Python: python -m venv venv and .\venv\Scripts\activate)

3. Install dependencies
Bash
uv pip install -r requirements.txt
4. Configure Environment Variables
This project requires a Google Gemini API key to run the LLM generation.

Get a free API key from Google AI Studio.

Create a new file named .env in the root folder of the project.

Copy the contents of .env.example into .env and replace the placeholder with your actual key:

Fragment de cod
GEMINI_API_KEY=your_actual_api_key_here
(Note: The .env file is git-ignored to keep your API key secure).

💻 Usage
Start the Application
To run the interactive web interface, ensure your virtual environment is active and run:

Bash
streamlit run app.py
Your default web browser will automatically open the application at http://localhost:8501.

Run the Evaluation Pipeline
Test the retrieval accuracy (Top-4 Hit Rate) and compare different chunk sizes:

Bash
python -m eval.run_eval

