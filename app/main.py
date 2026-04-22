from fastapi import FastAPI
from app.routers import items

app = FastAPI(title="Demo API", version="1.0.0")

app.include_router(items.router)


@app.get("/")
def root():
    return {"message": "FastAPI is running"}


@app.get("/health")
def health():
    return {"status": "ok"}
