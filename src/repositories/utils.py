from sqlalchemy import select, text, Integer
from sqlalchemy.sql import expression
from src.models.reservations import ReservationsORM


def check_for_reserv(date_from, date_to, table_id):
    query_count = (
        select(ReservationsORM.table_id)
        .select_from(ReservationsORM)
        .filter(
            ReservationsORM.table_id == table_id,
            ReservationsORM.date_from < date_to,
            (
                ReservationsORM.date_from
                + expression.cast(ReservationsORM.duration_minutes, Integer)
                * text("interval '1 minute'")
            )
            > date_from,
        )
    )
    return query_count
