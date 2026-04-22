from fastapi import APIRouter
from app.db.database import get_db
from app.services.query import llm
from app.models.schemas import SummarizeSectionRequest

router = APIRouter()




@router.post("/summarize-section")
def summarize_section(data: SummarizeSectionRequest):

    book_id = data.book_id
    topic = data.topic

    db = get_db()

    query = topic if topic else "summarize this document"

    existing = db.get(where={"book_id": book_id}, limit=1)

    if not existing["documents"]:
        return {
            "status": "error",
            "message": "Invalid book_id or book not indexed"
        }
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
Write a clear, natural, human-like summary of the content below.

RULES:
- Write in smooth paragraphs
- Do NOT use bullet points or markdown
- Keep it simple and clear
- Do NOT add anything outside the context

Focus: {topic if topic else "general overview"}

Context:
{context}

Summary:
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