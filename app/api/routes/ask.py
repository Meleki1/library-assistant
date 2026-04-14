from app.models.schemas import AskRequest
from app.services.query import ask_question
from fastapi import APIRouter
from app.core.state import book_status

router = APIRouter()




@router.post("/ask")
def ask_endpoint(request: AskRequest):
    if not request.question or request.question.strip() == "":
        return{
            "status": "error",
            "message": "question cannot be empty"
        }

    if request.book_id:
        if request.book_id not in book_status:
            return{
                "status": "error",
                "message": "book not found"
            }

        if book_status[request.book_id]["status"] != "completed":
            return{
                "status": "processing",
                "message": "book is still being processed"
            }
    
    answer = ask_question(
        question=request.question,
        book_id=request.book_id
        )

    return{
        "status": "success",
        "answer": answer
    }