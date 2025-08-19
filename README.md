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



## Notes
- For large corpora or multi-tenant use, consider external vector DBs (Pinecone, Weaviate, Chroma) and object storage (S3/GCS).
- Add auth (API keys/JWT) before exposing on the public internet.
```

