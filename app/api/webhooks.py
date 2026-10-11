from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.schemas.events import EventRequest, EventResponse
from app.db.session import get_db
from datetime import timezone
from app.models.events import IncomingEvent
from app.tasks import process_event


router=APIRouter(tags=["webhooks"])

@router.post('/webhooks/events', response_model=EventResponse, status_code=202)
def ingest_event(event: EventRequest, db: Session = Depends(get_db)):
    # Create a new IncomingEvent instance
    incoming_event = IncomingEvent(
        event_id=event.event_id,
        event_type=event.event_type.value,
        occurred_at=event.occurred_at.astimezone(timezone.utc),
        source=event.source,
        payload=event.payload.model_dump(mode="json"),
        status="pending"
    )
    # Add the new event to the database
    db.add(incoming_event)
    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to save the event to the database. Please try again later."
        )

    # Trigger the Celery task to process the event
    process_event.delay(event.event_id)

    return EventResponse(event_id=event.event_id, status="accepted", event_type=event.event_type)