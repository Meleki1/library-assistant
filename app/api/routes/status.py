from fastapi import APIRouter
from app.core.state import book_status

router = APIRouter()


@router.get("/book-status/{book_id}")
def get_book_status(book_id: str):

    if book_id not in book_status:
        return{
            "status": "error",
            "message": "book not found"
        }

    if book_status[book_id]["status"] != "completed":
        return{
            "status": "processing",
            "message": "Book still processing"
        }

    return{
        "book_id": book_id,
        **book_status[book_id]
    }