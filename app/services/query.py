from app.db.database import get_db
from langchain_openai import ChatOpenAI


llm = ChatOpenAI(model="gpt-4o-mini")


def ask_question(question: str, book_id: str = None):
    db = get_db()

    if book_id:
        results = db.similarity_search(
            question,
            k=5,
            filter={"book_id":book_id}
        )
    else:
        results = db.similarity_search(
            question,
            k=5
        )


    context_blocks = []

    for i, r in enumerate(results):
        book_name = r.metadata.get("book_name", "Unknown")

        block = f"[Source {i+1} | Book: {book_name}]\n{r.page_content}"
        context_blocks.append(block)
        

    context = "\n\n".join(context_blocks)

    prompt = f"""
    You are a controlled AI assistant for a digital library system.

    STRICT RULES (MANDATORY):
    - You MUST answer using ONLY the provided context.
    - You are NOT allowed to use prior knowledge, assumptions, or external information.
    - If the answer cannot be found explicitly in the context, respond EXACTLY with:
    "I don't know based on available books"
    - Do NOT guess, infer, fabricate, or introduce information not present in the context
    - You may rephrase or summarize the context for clarity
    - Do NOT use symbols like **, ##, -, or any markdown formatting


    RESPONSE STYLE:
    - Be clear, structured, and concise.
    - Make it feel like a human explanation and make it broad when explaining
    - Do not include opinions or extra commentary.
    - When answering, clearly structure your response:
    - Direct answer only when user ask for direct answer
    - Do NOT include sources in your answer
    - Sources will be added separately

    INTERNAL BEHAVIOR (DO NOT SHOW TO USER):
    1. Read the context carefully.
    2. Check if the answer can be derived directly from the context
    3. If YES → answer using only that information and cite sources.
    4. If NO → respond with the exact fallback sentence.
    

    Context:
    {context}

    Question:
    {question}

    Answer:

    """
    response = llm.invoke(prompt)
    answer = response.content

    sources = sorted(set(
    r.metadata.get("book_name", "Unknown") for r in results
    ))


    return{
        "answer": answer,
        "sources": sources
    }




    
