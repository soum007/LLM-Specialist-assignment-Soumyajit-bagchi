import os, tempfile, io, json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_upload_rejects_non_pdf():
    file = ("test.txt", io.BytesIO(b"hello"), "text/plain")
    r = client.post("/api/upload", files={"files": file})
    assert r.status_code == 415

def test_documents_endpoint():
    r = client.get("/api/documents")
    assert r.status_code == 200
    assert "documents" in r.json()
