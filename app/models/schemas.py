from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str
    book_id: str | None = None