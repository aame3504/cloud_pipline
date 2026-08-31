from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.model import User
from app.auth.web import router as auth_router
from app.database.database import Base
from app.database.database import engine
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
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(
    bind=engine
)


app.include_router(
    auth_router
)

app.include_router(
    imagerag_router
)


@app.get("/")
def root():
    return {
        "message": "Image RAG API",
        "docs": "/docs",
        "endpoints": {
            "signup": "/api/auth/signup",
            "login": "/api/auth/login",
            "me": "/api/auth/me",
            "logout": "/api/auth/logout",
            "image_rag": "/api/imagerag/search",
        },
    }