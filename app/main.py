import os
from fastapi import FastAPI
from app.provider import generate_answer

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "healthy", "version": os.getenv("APP_VERSION", "A")}


@app.get("/ask")
def ask(question: str):
    result = generate_answer(question)

    return {"version": os.getenv("APP_VERSION", "A"), **result}
