from fastapi import FastAPI
from app.api import chat, health

app = FastAPI(title="RAG with LangChain + FastAPI", version="0.1.0")

app.include_router(health.router)

