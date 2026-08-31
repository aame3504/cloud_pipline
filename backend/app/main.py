from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import IMAGE_DIR
from app.imagerag.web import router as imagerag_router


app = FastAPI(
    title="Image RAG API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    imagerag_router
)


app.mount(
    "/images",
    StaticFiles(
        directory=str(IMAGE_DIR)
    ),
    name="images",
)


@app.get("/")
def root():
    return {
        "message": "Image RAG API",
        "docs": "/docs",
        "endpoint": "/api/imagerag/search",
    }