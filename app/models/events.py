
from typing import Any

from sqlalchemy import JSON, DateTime, String
from sqlalchemy.orm import  Mapped, mapped_column
import datetime


from app.db.session import Base

class IncomingEvent(Base):
    __tablename__ = "incoming_events"

    event_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    event_type: Mapped[str] = mapped_column(String(255), nullable=False)
    occurred_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    received_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")