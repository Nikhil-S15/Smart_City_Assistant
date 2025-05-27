
# Smart City Information Assistant 🏙️

An AI-powered chatbot for answering citizen queries about city services, facilities, transportation, and policies using RAG (Retrieval-Augmented Generation) with ChromaDB and Ollama.

## Features

- Answers questions about:
  - City services (permits, waste collection, utilities)
  - Public facilities (libraries, parks, hospitals)
  - Transportation (bus routes, parking, traffic)
  - City policies and regulations
  - Emergency information
- Conversation history
- Source document references
- Easy-to-use web interface

## Tech Stack

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Vector Database**: ChromaDB
- **LLM**: Ollama with LLaMA 3
- **Embeddings**: OllamaEmbeddings
- **LangChain**: RAG pipeline orchestration

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.ai/) installed and running
- LLaMA 3 model downloaded (`ollama pull llama3`)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/smart-city-assistant.git
   cd smart-city-assistant
Create and activate virtual environment:
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:
bash
pip install -r backend/requirements.txt -r frontend/requirements.txt
Download the LLaMA 3 model:
bash
ollama pull llama3
Setup

Process the knowledge base data:
bash
python scripts/process_data.py
Initialize ChromaDB vector store:
bash
python scripts/setup_vector_db.py
Running the Application

Start the backend API:
bash
cd backend
uvicorn app.main:app --reload
In a new terminal, start the frontend:
bash
cd frontend
streamlit run app.py
Access the application at:
Frontend: http://localhost:8501
Backend API: http://localhost:8000
Project Structure

smart-city-assistant/
├── backend/               # FastAPI backend
│   ├── app/               # Application code
│   └── requirements.txt   # Backend dependencies
├── frontend/              # Streamlit frontend
│   ├── app.py             # UI code
│   └── requirements.txt   # Frontend dependencies
├── data/
│   ├── processed/         # Processed data chunks
│   └── raw/               # Original JSON data
├── scripts/               # Data processing scripts
├── .env                   # Environment variables
└── README.md              # This file
Configuration

Edit .env for custom settings:

ini
CHROMA_DB_PATH=data/chroma_db
OLLAMA_MODEL=llama3
API_HOST=0.0.0.0
API_PORT=8000
Troubleshooting

Common Issues:

Import errors:
Ensure all dependencies are installed
Try pip install --upgrade -r backend/requirements.txt
ChromaDB not persisting:
Delete and recreate the vector store:
bash
rm -rf data/chroma_db
python scripts/setup_vector_db.py
Ollama connection issues:
Verify Ollama is running: ollama list
Check model is downloaded: ollama pull llama3
Future Enhancements

Add user authentication
Support PDF/document uploads
Multi-language support
SMS/WhatsApp integration
