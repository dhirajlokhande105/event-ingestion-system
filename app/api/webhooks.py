from fastapi import APIRouter
from app.schemas.events import EventRequest, EventResponse
from uuid import uuid4

router=APIRouter(tags=["webhooks"])

@router.post('/webhooks/events', response_model=EventResponse, status_code=202)
def ingest_event(event: EventRequest):
    return EventResponse(event_id=event.event_id or str(uuid4()), status="accepted", event_type=event.event_type)