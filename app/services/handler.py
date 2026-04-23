from app.api.routes.ask import ask_logic
from app.api.routes.summarize import summarize_logic
from app.api.routes.summarizeSection import summarize_section_logic


def handle_ask(message, book_id):
    return ask_logic(message, book_id)

def handle_summarize(book_id=None, instruction=None):
    return summarize_logic(book_id, instruction)

def handle_summarize_section(message, book_id):
    return summarize_section_logic(
        book_id=book_id,
        topic=message
    )



