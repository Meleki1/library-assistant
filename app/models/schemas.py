from pydantic import BaseModel
from typing import Optional


class AskRequest(BaseModel):
    question: str
    book_id: str | None = None


class SummarizeRequest(BaseModel):
    book_id: Optional[str] = None
    instruction: Optional[str] = None

class SummarizeSectionRequest(BaseModel):
    book_id: str
    topic: Optional[str] = None 

class ChatRequest(BaseModel):
    message: str
    book_id: str | None = None