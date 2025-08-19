import argparse, os
from app.rag import upsert_documents

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--files", nargs="+", required=True, help="List of PDF files to ingest")
    args = parser.parse_args()
    res = upsert_documents(args.files)
    print(res)
