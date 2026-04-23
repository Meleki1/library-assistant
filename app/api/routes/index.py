import time
import hashlib
from fastapi import UploadFile, File, BackgroundTasks
from fastapi import APIRouter
from app.core.state import book_status
from app.services.pipeline import process_book

router = APIRouter()



def generate_book_id(file_name: str):
    return hashlib.md5(file_name.encode()).hexdigest()

@router.post ("/index_book")
async def index_book(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    book_id = generate_book_id(file.filename)
    file_path = f"documents/{int(time.time())}_{file.filename}"
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)


    book_status[book_id] = {
        "status": "processing",
        "stage": "starting"
    }

    background_tasks.add_task(
        process_book_background, 
        book_id, file_path 
        )

    return{
        "book_status": "processing",
        "book_id": book_id,
        "message": "Book upload started"
    }


def process_book_background(book_id, file_path):
    try:
        book_status[book_id]["stage"] = "processing"

        process_book(book_id, file_path)

        book_status[book_id] = {
            "status": "completed",
            "stage": "done"
        }
    except Exception as e:
        book_status[book_id] = {
            "status": "failed",
            "message": str(e)
        }
