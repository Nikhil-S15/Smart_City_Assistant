from langchain.embeddings import OllamaEmbeddings  # Stable import
from langchain.vectorstores import Chroma  # Stable import
import json
from pathlib import Path
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from backend.app.config import settings
except ImportError:
    # Fallback configuration if config import fails
    class Settings:
        chroma_db_path = "data/chroma_db"
        ollama_model = "llama3"
    settings = Settings()

def setup_chromadb():
    # Use the updated OllamaEmbeddings
    embeddings = OllamaEmbeddings(model=settings.ollama_model)
    
    with open("data/processed/chunks.json", "r") as f:
        chunks_data = json.load(f)
    
    texts = [item["text"] for item in chunks_data]
    metadatas = [item["metadata"] for item in chunks_data]
    
    # Create ChromaDB vector store
    vector_store = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory=settings.chroma_db_path
    )
    
    print(f"✅ ChromaDB initialized at {settings.chroma_db_path}")

if __name__ == "__main__":
    Path(settings.chroma_db_path).mkdir(parents=True, exist_ok=True)
    setup_chromadb()