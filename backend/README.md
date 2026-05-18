# AI Codebase Chatbot Backend

This is the FastAPI backend for the AI Codebase Chatbot project. It uses Retrieval-Augmented Generation (RAG) to ingest GitHub repositories and answer questions about the code.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   - Windows: `.\venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

Start the local development server:
```bash
uvicorn app.main:app --reload
```

## API Documentation
Once running, the interactive API documentation (Swagger) is available at:
http://127.0.0.1:8000/docs
