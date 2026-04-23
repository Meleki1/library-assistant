from fastapi import APIRouter
from app.db.database import get_db
from app.services.query import llm
from app.models.schemas import SummarizeSectionRequest
from app.core.state import book_status

router = APIRouter()

@router.post("/summarize-section")
def summarize_section(data: SummarizeSectionRequest):
    return summarize_section_logic(data.book_id, data.topic)


def summarize_section_logic(book_id: str, topic: str | None = None):

    db = get_db()

   
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
    else:
        return {
            "status": "error",
            "message": "book_id is required"
        }

    
    query = f"{topic} summary" if topic else "general overview"

    results = db.similarity_search(
        query,
        k=8,
        filter={"book_id": book_id}
    )

    if not results:
        return {
            "status": "error",
            "message": "No relevant content found"
        }

    
    context = "\n\n".join(r.page_content for r in results)

    
    prompt = f"""
You are an AI assistant.

TASK:
Write a clear, natural, human-like explanation of the content below.

RULES:
- Write in smooth paragraphs
- Do NOT use bullet points or markdown
- Keep it simple and easy to understand
- Do NOT add anything outside the context
- Explain like you're teaching a student

Focus: {topic if topic else "general overview"}

Context:
{context}

Response:
"""

    response = llm.invoke(prompt)
    summary = response.content

    sources = list(set(
        r.metadata.get("book_name", "Unknown")
        for r in results
    ))

    return {
        "status": "success",
        "topic": topic if topic else "general",
        "summary": summary,
        "sources": sources
    }