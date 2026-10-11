from app.db.session import Base
from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal


class Listing(Base):

    __tablename__ = "listings"

    listing_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    city: Mapped[str | None] = mapped_column(String(255), nullable=True)