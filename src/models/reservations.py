from black import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, SmallInteger, String
from src.database import BaseModelORM


class ReservationsORM(BaseModelORM):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, unique=True)
    customer_name: Mapped[str] = mapped_column(String(length=100))
    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id"))
    date_from: Mapped[datetime]
    duration_minutes: Mapped[int]
