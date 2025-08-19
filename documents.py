import os
from fastapi import APIRouter

router = APIRouter(tags=["documents"])

@router.get("/documents")
def list_documents():
    if not os.path.exists("data"):
        return {"documents": []}
    return {"documents": sorted([f for f in os.listdir("data") if f.lower().endswith(".pdf")])}
