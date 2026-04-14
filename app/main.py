from fastapi import FastAPI
from app.api.routes import index, ask, status,debug





app = FastAPI()
book_status = {}




app.include_router(debug.router)
app.include_router(index.router)
app.include_router(ask.router)
app.include_router(status.router)














