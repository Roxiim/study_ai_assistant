"""PDF text extraction and smart chunking. Page numbers are kept as metadata."""
from pathlib import Path
import fitz  # PyMuPDF

def extract_pages(pdf_path: str | Path) -> list[dict]:
    """Return one dict per non-empty page: source file, page number, text."""
    doc = fitz.open(str(pdf_path))
    name = Path(pdf_path).name
    pages = []
    
    for number, page in enumerate(doc, start=1):
        text = (page.get_text() or "").strip()
        if text:
            pages.append({"source": name, "page": number, "text": text})
            
    return pages

def chunk_text(text: str, size: int = 800, overlap: int = 100) -> list[str]:
    """
    Split text into pieces of ~`size` characters.
    It intelligently looks for the last space to avoid cutting words in half.
    """
    if overlap >= size:
        raise ValueError("overlap must be smaller than size")
        
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + size
        
        if end < len(text):
            last_space = text.rfind(" ", start, end)
            if last_space != -1 and last_space > start:
                end = last_space
                
        piece = text[start:end].strip()
        if piece:
            chunks.append(piece)
            
        start = end - overlap
        
    return chunks

def chunk_pdf(pdf_path: str | Path, size: int = 800, overlap: int = 100) -> list[dict]:
    """Extract and chunk a PDF. Chunks never cross page boundaries."""
    chunks = []
    for page in extract_pages(pdf_path):
        for i, piece in enumerate(chunk_text(page["text"], size, overlap)):
            chunks.append({
                "id": f"{page['source']}-p{page['page']}-c{i}",
                "text": piece,
                "source": page["source"],
                "page": page["page"],
            })
    return chunks