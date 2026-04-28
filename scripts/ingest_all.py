"""
Run from the project root:  python scripts/ingest_all.py
Ingests every PDF in data/raw/ into the Chroma vector store.
Already-ingested documents are skipped.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.ingest_service import IngestService

RAW_DIR = "data/raw"


def main():
    service = IngestService()
    pdfs = [f for f in os.listdir(RAW_DIR) if f.endswith(".pdf")]

    if not pdfs:
        print(f"No PDFs found in {RAW_DIR}/")
        return

    for filename in pdfs:
        path = os.path.join(RAW_DIR, filename)
        try:
            result = service.ingest_document(path)
            print(f"[OK]      {filename}  ({result['chunks_created']} chunks)")
        except ValueError as e:
            print(f"[SKIPPED] {filename}  ({e})")
        except Exception as e:
            print(f"[ERROR]   {filename}  ({e})")


if __name__ == "__main__":
    main()
