from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from ..rag import retrieve, build_prompt
from ..providers.llm_provider import get_llm

router = APIRouter(tags=["query"])

class QueryRequest(BaseModel):
    question: str
    top_k: int = 4

@router.post("/query")
def ask(req: QueryRequest) -> Dict[str, Any]:
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    docs = retrieve(req.question, k=req.top_k)
    contexts = [d.page_content for d in docs]
    prompt = build_prompt(req.question, contexts)
    llm = get_llm()
    answer = llm.generate(prompt)
    sources = [{"source": str(d.metadata.get("source")), "page": d.metadata.get("page")} for d in docs]
    return {"answer": answer, "sources": sources}
