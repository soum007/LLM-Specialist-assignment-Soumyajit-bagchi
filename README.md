# RAG Pipeline (FastAPI + FAISS)

A production-ready Retrieval-Augmented Generation (RAG) API that lets users upload documents (PDF), builds a vector index (FAISS) with Sentence-Transformers embeddings, and answers questions with pluggable LLM providers (OpenAI, Gemini, HuggingFace Inference).

## Features
- Upload up to 20 PDFs per request (1000 pages per file supported by the loaders).
- Chunking via RecursiveCharacterTextSplitter (configurable).
- Embedding with sentence-transformers (default: all-MiniLM-L6-v2).
- Vector store: FAISS (local, persisted).
- Pluggable LLM providers via `LLM_PROVIDER`: `openai`, `google`, `hf`.
- REST API: `/api/upload`, `/api/query`, `/api/documents`.
- Dockerized with Docker Compose for local/cloud deploys.
- Basic tests with pytest + TestClient.

## Quickstart

```bash
cp .env.example .env  # fill in keys
docker compose up --build
# API at http://localhost:8000
```

### Local (no Docker)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API

- `POST /api/upload` (multipart form)
  - field name: `files` (repeatable), PDFs only.
- `POST /api/query`
  - body: `{ "question": "your question", "top_k": 4 }`
- `GET /api/documents`

OpenAPI docs at `/docs`.

## Switch LLM Provider
Set `LLM_PROVIDER` in `.env`:
- `openai`: needs `OPENAI_API_KEY`, optional `OPENAI_MODEL`.
- `google`: needs `GOOGLE_API_KEY`, optional `GOOGLE_MODEL`.
- `hf`: needs `HF_TOKEN`, optional `HF_REPO_ID`.

## Testing
```bash
pytest -q
```

## Notes
- For large corpora or multi-tenant use, consider external vector DBs (Pinecone, Weaviate, Chroma) and object storage (S3/GCS).
- Add auth (API keys/JWT) before exposing on the public internet.
```

