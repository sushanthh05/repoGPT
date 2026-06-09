# RepoGPT Backend

This backend now focuses on Phase 2: accepting a GitHub repository URL, validating it, cloning it locally, and storing repository metadata for later parsing.

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

## Phase 2 API

`POST /api/repositories/analyze`

Request body:

```json
{
   "repo_url": "https://github.com/vercel/next.js"
}
```

`GET /api/repositories`

Returns the repositories that have already been cloned by the backend.

## API Documentation

Once running, the interactive API documentation (Swagger) is available at:

http://127.0.0.1:8000/docs

## Storage

- Cloned repositories live in `backend/repositories/`
- Metadata is persisted in `backend/repository_metadata.json`
- Duplicate URLs are reused instead of cloned again

## Dependencies

Install `GitPython` alongside the existing FastAPI stack to enable cloning.
