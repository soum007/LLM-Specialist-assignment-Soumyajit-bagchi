import os
from typing import List, Tuple, Dict, Any
from dotenv import load_dotenv
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import BaseModel

load_dotenv()

DATA_DIR = os.getenv("DATA_PATH", "data")
DB_FAISS_PATH = os.getenv("DB_FAISS_PATH", "vectorstore/db_faiss")
EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# ------- Embeddings / Vector Store -------
def _embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL)

def load_or_create_vectorstore():
    if os.path.exists(DB_FAISS_PATH) and any(p.endswith(".faiss") for p in os.listdir("vectorstore")):
        return FAISS.load_local(DB_FAISS_PATH, _embeddings(), allow_dangerous_deserialization=True)
    # If none exists yet, create an empty one by embedding an empty doc list (FAISS requires data)
    return None

def create_chunks(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    return splitter.split_documents(docs)

def embed_chunks(chunks):
    db = FAISS.from_documents(chunks, _embeddings())
    db.save_local(DB_FAISS_PATH)
    return db

def upsert_documents(filepaths: List[str]) -> Dict[str, Any]:
    from langchain_community.document_loaders import DirectoryLoader
    from langchain.schema import Document

    docs = []
    for fp in filepaths:
        loader = PDFPlumberLoader(fp)
        docs.extend(loader.load())

    chunks = create_chunks(docs)
    # If existing store present, merge
    if os.path.exists(DB_FAISS_PATH) and any(p.endswith(".faiss") for p in os.listdir("vectorstore")):
        existing = FAISS.load_local(DB_FAISS_PATH, _embeddings(), allow_dangerous_deserialization=True)
        new = FAISS.from_documents(chunks, _embeddings())
        existing.merge_from(new)
        existing.save_local(DB_FAISS_PATH)
        db = existing
    else:
        db = embed_chunks(chunks)

    return {"files": [os.path.basename(p) for p in filepaths], "chunks_indexed": len(chunks)}

def retrieve(query: str, k: int = 4):
    db = FAISS.load_local(DB_FAISS_PATH, _embeddings(), allow_dangerous_deserialization=True)
    return db.similarity_search(query, k=k)

# Prompting
SYSTEM_HINT = "Use only the provided context to answer. If unsure, say you don't know."
def build_prompt(question: str, contexts: List[str]) -> str:
    joined = "\n\n---\n".join(contexts)
    return f"""{SYSTEM_HINT}

Context:
{joined}

Question: {question}

Answer succinctly based only on the context above."""
