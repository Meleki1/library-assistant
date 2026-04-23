AI Digital Library Backend

Overview
This project is an AI-powered digital library system that allows users to select books from the application and ask questions based on their content.

The system processes books into chunks, stores them in a vector database, and retrieves relevant information to generate answers.

Features
Upload and index books (PDF, DOCX, TXT)
Ask questions across all books or a specific book
Source attribution (shows which book the answer came from)
Bulk indexing for existing books on the application


Project Structure
app/
  ├── api/          # API routes
  ├── services/     # Processing logic
  ├── utils/        # Document loaders & text splitting
  ├── db/           # Database connection
  ├── scripts/      # Bulk indexing script

Installation
1. Clone the repository
git clone <https://github.com/Meleki1/library-assistant.git>
cd ai_library
2. Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
3. Install dependencies
pip install -r requirements.txt
Running the Application
uvicorn app.main:app --reload

API will be available at:

http://127.0.0.1:8000/docs
Bulk Indexing (IMPORTANT)

Before using the AI system, all existing books must be indexed.

Run:

python -m app.scripts.index_existing_books

This processes all books and stores them in the vector database.

API Endpoints
1. Index Book
POST /index-book

Upload a book file for processing.

2. Check Book Status
GET /book-status/{book_id}

Check if a book has finished processing.

3. Ask Question
POST /ask

Request body:

{
  "question": "What is journalism?",
  "book_id": "optional"
}
Important Notes
-Books must be indexed before querying
-book_id is used internally for filtering
-book_name is used for displaying sources
-Bulk indexing should be run once after deployment

Development Notes
-Debug endpoints are enabled only in development mode
-CORS is open for local testing and should be restricted in production

Future Improvements
-Chapter-based querying
-Authentication & user-specific access



