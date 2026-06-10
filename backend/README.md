# RepoGPT Backend

This backend now focuses on Phase 2 and Phase 3: accepting a GitHub repository URL, validating it, cloning it locally, and parsing repository files into structured documents.

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

## Phase 3 API

`POST /api/repositories/{repository_id}/parse`

This scans a cloned repository, filters files, reads file contents, and stores parsed documents in `backend/parsed_documents.json`.

Response example:

```json
{
   "status": "success",
   "repository_id": "repo_8f3a7c",
   "documents_created": 148,
   "message": "Repository parsed successfully"
}
```

## Parsed Output

Each parsed document contains:

- `document_id`
- `repository_id`
- `filename`
- `file_path`
- `language`
- `file_extension`
- `content`
- `size`
- `created_at`

The parser currently ignores:

- directories like `.git`, `node_modules`, `dist`, `build`, `coverage`, `out`, `venv`, `__pycache__`, `.cache`, `.idea`, `.vscode`, and `.next`
- binary or low-value file types like images, videos, executables, libraries, and lock files
- files larger than 1 MB

Supported file types at this stage:

- `.py`, `.js`, `.ts`, `.jsx`, `.tsx`, `.java`, `.md`, `.json`, `.html`, `.css`

## API Documentation

Once running, the interactive API documentation (Swagger) is available at:

http://127.0.0.1:8000/docs

## Storage

- Cloned repositories live in `backend/repositories/`
- Metadata is persisted in `backend/repository_metadata.json`
- Parsed documents are persisted in `backend/parsed_documents.json`
- Duplicate URLs are reused instead of cloned again

## Dependencies

Install `GitPython` alongside the existing FastAPI stack to enable cloning.
