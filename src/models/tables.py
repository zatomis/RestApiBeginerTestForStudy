from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, SmallInteger
from src.database import BaseModelORM


class TablesORM(BaseModelORM):
    __tablename__ = "tables"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(length=100))
    seats: Mapped[int] = mapped_column(SmallInteger)
    location: Mapped[str] = mapped_column()
