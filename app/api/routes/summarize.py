from fastapi import APIRouter
from app.db.database import get_db
from app.services.query import llm
from app.models.schemas import SummarizeRequest

router = APIRouter()


@router.post("/summarize")
def summarize_book(data: SummarizeRequest):

    book_id = data.book_id
    instruction = data.instruction or "Provide a clear summary."

    db = get_db()
    
    if book_id:
        existing = db.get(where={"book_id": book_id}, limit=1)

    if not existing["documents"]:
        return {
            "status": "error",
            "message": "Invalid book_id or book not indexed"
        }

    if book_id:
        results = db.similarity_search(
            "summarize this book",
            k=8,
            filter={"book_id": book_id}
        )
    else:
        results = db.similarity_search(
            "summarize this book",
            k=8
        )

    if not results:
        return {
            "status": "error",
            "message": "I don't know based on available books"
        }

    context = "\n\n".join(
        r.page_content for r in results
    )

    prompt = f"""
You are an AI assistant.

TASK:
Write a clear, natural, and human-like summary of the content below.

RULES:
- Write in smooth paragraphs (not bullet points)
- Do NOT use symbols like **, ##, -, or any markdown formatting
- Do NOT use headings
- Make it feel like a human explanation
- Keep it simple, clear, and engaging
- Do NOT add information outside the context
-Write as if explaining to a student in a calm and conversational tone.

{instruction}

Context:
{context}

Summary:
"""

    response = llm.invoke(prompt)
    summary = response.content

    if book_id:
        sources = [results[0].metadata.get("book_name", "Unknown")]
    else:
        sources = list(set(
            r.metadata.get("book_name", "Unknown")
            for r in results
    ))

    return {
        "status": "success",
        "summary": summary,
        "sources": sources
    }