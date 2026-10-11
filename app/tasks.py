from decimal import Decimal

from app.celery_app import celery_app
from app.db.session import SessionLocal
from app.models.events import IncomingEvent
from app.models.listings import Listing


@celery_app.task(name="process_event")
def process_event(event_id: str) -> None:
    with SessionLocal() as session:
        event = session.get(IncomingEvent, event_id)
        if event is None:
            return

        listing_id = event.payload["listing_id"]
        listing = session.get(Listing, listing_id)

        if listing is None:
            listing = Listing(listing_id=listing_id)
            session.add(listing)

        price = event.payload.get("price")
        if price is not None:
            listing.price = Decimal(str(price))

        status = event.payload.get("status")
        if status is not None:
            listing.status = status

        city = event.payload.get("city")
        if city is not None:
            listing.city = city

        event.status = "processed"
        session.commit()