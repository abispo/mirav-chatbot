from fastapi import FastAPI
from app.routes.events import router as events_router
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(title="Mirav Perfumes API")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(events_router)