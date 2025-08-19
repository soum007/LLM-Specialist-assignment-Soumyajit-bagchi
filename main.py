import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import ingest, query, documents

app = FastAPI(title="RAG Pipeline API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router, prefix="/api")
app.include_router(query.router, prefix="/api")
app.include_router(documents.router, prefix="/api")

@app.get("/")
def health():
    return {"status": "ok", "message": "RAG API running"}
