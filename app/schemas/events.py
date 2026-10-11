from pydantic import BaseModel, ConfigDict, Field, AwareDatetime
from enum import Enum


class StatusType(str, Enum):
    ACTIVE = "active"
    PENDING = "pending"
    SOLD = "sold"
    OFF_MARKET = "off_market"

class EventType(str, Enum):
    LISTING_CREATED = "listing.created"
    LISTING_UPDATED = "listing.updated"
    LISTING_STATUS_CHANGED = "listing.status_changed"

class EventPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    listing_id: str
    price: float | None = Field(default=None, gt=0)
    status: StatusType | None = Field(default=None, description="The status of the listing")
    city: str | None = None


class EventRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    event_id: str
    event_type: EventType = Field(description="The type of the event")
    occurred_at: AwareDatetime
    source: str = Field(min_length = 1, description="The source of the event")
    payload: EventPayload


class EventResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    event_id: str = Field(description="The ID of the event")
    status: str = Field(description="The status of the event")
    event_type: str = Field(description="The type of the event")

