from fastapi import APIRouter
from app.models.schemas import ChatRequest
from app.services.handler import handle_ask,handle_summarize, handle_summarize_section
from app.core.intent import classify_intent


router = APIRouter()

@router.post("/chat")
def chat(data: ChatRequest):

    message = data.message
    book_id = data.book_id

    intent = classify_intent(message)

    
    if intent == "question":
        return handle_ask(message, book_id)

    elif intent == "summarize":
        return handle_summarize(
            book_id=book_id,
            instruction=message
        )

    elif intent == "summarize_section":
        return handle_summarize_section(message, book_id)

    else:
        return {
            "status": "error",
            "message": "Could not understand request"
        }