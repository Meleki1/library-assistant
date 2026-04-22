import os
from app.services.pipeline import process_book
from app.db.database import get_db

BOOKS_FOLDER = "documents"
processed_books = set()



def get_all_books(folder_path):
    books = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            book_id = os.path.splitext(filename)[0]

            books.append({
                "book_id": book_id,
                "file_path": file_path
            })

    return books




def index_all_books():

    books = get_all_books(BOOKS_FOLDER)

    print(f"Found {len(books)} books to process\n")

    db = get_db()

    for i, book in enumerate(books, start=1):

        book_id = book["book_id"]
        file_path = book["file_path"]

        existing = db.get(where={"book_id": book_id})

        if existing and existing.get("documents"):
            print(f"⏭ Already indexed: {book_id}")
            continue

        print(f"[{i}/{len(books)}] Processing: {file_path}")

        try:
            process_book(book_id, file_path)
            print(f"✅ Success: {book_id}\n")

        except Exception as e:
            print(f"❌ Failed: {book_id} → {e}\n")


if __name__ == "__main__":
    index_all_books()