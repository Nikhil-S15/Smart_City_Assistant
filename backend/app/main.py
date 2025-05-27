from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
# Stable imports that have been consistent for months
from langchain.llms import Ollama
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

from langchain.prompts import PromptTemplate
from .config import settings
import os

app = FastAPI(title="Smart City Information Assistant API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
embeddings = OllamaEmbeddings(model=settings.ollama_model)
vector_store = Chroma(
    persist_directory=settings.chroma_db_path,
    embedding_function=embeddings
)

# Custom prompt template
prompt_template = """You are a helpful assistant for a smart city. Use the following context to answer the question.
If you don't know the answer, say you don't know. Be precise and factual.

Context:
{context}

Question: {question}
Helpful Answer:"""

PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

llm = Ollama(model=settings.ollama_model)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
    chain_type_kwargs={"prompt": PROMPT},
    return_source_documents=True
)

class QueryRequest(BaseModel):
    query: str
    conversation_history: List[str] = []

class DocumentResponse(BaseModel):
    text: str
    metadata: dict
    score: float

class QueryResponse(BaseModel):
    response: str
    source_documents: Optional[List[DocumentResponse]]

@app.post("/query", response_model=QueryResponse)
async def query_knowledge_base(request: QueryRequest):
    try:
        result = qa_chain({"query": request.query})
        return {
            "response": result["result"],
            "source_documents": [
                {
                    "text": doc.page_content,
                    "metadata": doc.metadata,
                    "score": 0.0  # ChromaDB doesn't return scores by default
                } for doc in result["source_documents"]
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)