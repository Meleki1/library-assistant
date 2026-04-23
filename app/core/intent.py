from app.services.query import llm

def classify_intent(message: str):
    prompt = f"""
Classify the user request into one of these:

- question
- summarize
- summarize_section

Return ONLY one word.

Message:
{message}
"""

    response = llm.invoke(prompt)
    return response.content.strip().lower()