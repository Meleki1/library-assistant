import os
import re
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from pypdf import PdfReader
from docx import Document




load_dotenv()
embeddings = OpenAIEmbeddings()


def load_document(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        reader = PdfReader(file_path)
        full_text = ""

        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
        return full_text

    elif ext == ".docx":
        doc = Document(file_path)
        full_text = ""
        for para in doc.paragraphs:
            full_text += para.text + "\n"
        return full_text

    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8")as f:
            return f.read()
    else:
        raise ValueError(f"unsupported format type{ext}")



def split_text(full_text, chunk_size=3000):
    chunk = []
    for i in range(0, len(full_text), chunk_size):
        chunk.append(full_text[i:i+chunk_size])
    return chunk

def store_embeddings(chunks, file_location):
    db = Chroma(
        collection_name="documents", 
        embedding_function=embeddings, 
        persist_directory="db"
        )

    db.add_texts(
        chunks, 
        metadatas=[{"source": file_location}] * len(chunks)
        )

