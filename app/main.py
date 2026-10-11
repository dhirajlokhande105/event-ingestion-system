from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.webhooks import router as webhooks_router
from app.models.events import IncomingEvent
from app.db.session import engine, Base
from app.models.listings import Listing

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title = "Event Ingestion Engine")
app.include_router(health_router)
app.include_router(webhooks_router)

@app.get("/")
def root():
    return {"message": "Welcome to Application"}
