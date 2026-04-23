import hashlib



book_status = {}
def generate_book_id(file_name: str):
    return hashlib.md5(file_name.encode()).hexdigest()