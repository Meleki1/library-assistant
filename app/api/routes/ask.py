from app.models.schemas import AskRequest
from app.services.query import ask_question
from fastapi import APIRouter
from app.core.state import book_status
from app.db.database import get_db

router = APIRouter()




@router.post("/ask")
def ask_endpoint(data: AskRequest):
    return ask_logic(data.question, data.book_id)




def ask_logic(question: str, book_id: str | None = None):

    db = get_db()

    if not question or question.strip() == "":
        return {
            "status": "error",
            "message": "question cannot be empty"
        }

    if book_id:
        existing = db.get(where={"book_id": book_id}, limit=1)

        if not existing["documents"]:
            return {
                "status": "error",
                "message": "Invalid book_id or book not indexed"
            }

        
        if book_id in book_status:
            if book_status[book_id]["status"] != "completed":
                return {
                    "status": "processing",
                    "message": "book is still being processed"
                }

    answer = ask_question(
        question=question,
        book_id=book_id
    )

    return {
        "status": "success",
        "answer": answer
    }