from fastapi import FastAPI
from app.api.routes import index, ask, status,debug
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()



app.include_router(debug.router)
app.include_router(index.router)
app.include_router(ask.router)
app.include_router(status.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # enter origin in production ["https://yourfrontend.com"] instead of ["*"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)














