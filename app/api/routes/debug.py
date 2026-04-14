import os
from fastapi import APIRouter
from app.db.database import get_db


router = APIRouter()
DEBUG_MODE = os.getenv("DEBUG_MODE", "false") == "true"

if DEBUG_MODE:
    @router.get("/debug/books")
    def list_books():

        db = get_db()

        results = db.get()

        books = {}

        for meta in results["metadatas"]:
            book_id = meta.get("book_id")
            book_name = meta.get("book_name", "Unknown")

            if book_id not in books:
                books[book_id] = {
                    "book_name": book_name,
                    "chunk_count": 0
                }

            books[book_id]["chunk_count"] += 1

        return {
            "total_books": len(books),
            "books": [
                {
                    "book_id": bid,
                    "book_name": data["book_name"],
                    "chunk_count": data["chunk_count"]
                }
                for bid, data in books.items()
            ]
        }

    @router.get("/debug/all-chunks")
    def get_all_chunks():

        db = get_db()

        results = db.get()

        chunks = []

        for doc, meta in zip(results["documents"], results["metadatas"]):
            chunks.append({
                "text": doc,
                "book_id": meta.get("book_id"),
                "book_name": meta.get("book_name", "Unknown")
            })

        return {
            "total_chunks": len(chunks),
            "chunks": chunks
        }