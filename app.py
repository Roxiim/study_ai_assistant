import streamlit as st
import os
from src.ingest import chunk_pdf
from src.embed import get_collection, add_chunks
from src.answer import answer

os.makedirs("data", exist_ok=True)

st.set_page_config(page_title="Study Assistant RAG", page_icon="📚")

st.title("📚 Study Assistant RAG")
st.markdown("Upload your course PDFs and ask questions. The AI will strictly answer based on your documents.")

with st.sidebar:
    st.header("1. Upload Documents")
    uploaded_files = st.file_uploader("Upload course PDFs", type=["pdf"], accept_multiple_files=True)
    
    if st.button("Process & Update Database"):
        if uploaded_files:
            with st.spinner("Saving files and generating embeddings..."):
                collection = get_collection()
                
                for uploaded_file in uploaded_files:
                    file_path = os.path.join("data", uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    chunks = chunk_pdf(file_path, size=800, overlap=100)
                    
                    
                    add_chunks(collection, chunks)
                    
                st.success("Database updated successfully!")
        else:
            st.warning("Please upload some PDFs first.")

st.header("2. Ask Questions")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("E.g., What is a projection transformation?"):

    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Searching documents and thinking..."):
            try:
                collection = get_collection()
                ans, passages = answer(collection, prompt)
                
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            except Exception as e:
                error_msg = f"An error occurred: {str(e)}"
                st.error(error_msg)