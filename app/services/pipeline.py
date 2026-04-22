import os
from app.utlis import load_document, split_text
from app.db.database import get_db



def process_book(book_id, file_path):

    book_name = os.path.splitext(os.path.basename(file_path))[0].replace("_", " ")

    text = load_document(file_path)

    chunks = split_text(text)  

    db = get_db()

    metadatas = [
        {
            "book_id": book_id,
            "book_name": book_name
        }
        for _ in chunks
    ]

    db.add_texts(chunks, metadatas=metadatas)

    print(f"Book {book_id} processed successfully")

