"""
Run from the project root:  python scripts/clear_vectordb.py
Options:
  --all             clear everything
  --source <name>   delete a single document by filename
  --list            show what's currently ingested
"""

import os
import sys
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.vectorstore.chroma_store import ChromaStore


def main():
    parser = argparse.ArgumentParser(description="Manage the vector database")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="Clear all documents")
    group.add_argument("--source", type=str, help="Delete a specific document by filename")
    group.add_argument("--list", action="store_true", help="List all ingested documents")
    args = parser.parse_args()

    store = ChromaStore()

    if args.list:
        sources = store.list_sources()
        if not sources:
            print("No documents ingested.")
        else:
            print(f"{len(sources)} document(s) in vector store:")
            for s in sources:
                print(f"  - {s}")

    elif args.source:
        deleted = store.delete_source(args.source)
        if deleted == 0:
            print(f"[NOT FOUND] '{args.source}' — no chunks matched.")
        else:
            print(f"[DELETED] '{args.source}' — {deleted} chunks removed.")

    elif args.all:
        confirm = input("This will delete ALL ingested documents. Type 'yes' to confirm: ")
        if confirm.strip().lower() == "yes":
            deleted = store.clear_all()
            print(f"[CLEARED] {deleted} chunks removed.")
        else:
            print("Aborted.")


if __name__ == "__main__":
    main()
