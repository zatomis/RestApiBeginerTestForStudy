from fastapi import APIRouter, Body
from src.api.dependencies import DBDep
from src.exceptions import (
    ObjectNotFoundException,
    TableNotFoundHTTPException,
    ReservationsNotFoundHTTPException,
    TableIsNotAvailableHTTPException,
)
from src.schemas.reservations import ReservationAdd
from datetime import timedelta
import logging

router = APIRouter(prefix="/reservations", tags=["Бронирование 💸"])


@router.get("/")
async def get_reservations(db: DBDep):
    reservations = await db.reservations.get_all()
    return {"data": reservations}


@router.post(
    "/", summary="Добавить данные", description="<H1>Забронировать столик</H1>"
)
async def create_reservations(
    db: DBDep,
    reservations_data: ReservationAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Бронь №1",
                "value": {
                    "customer_name": "Петров А.В.",
                    "table_id": 100,
                    "date_from": "2025-10-01 10:20",
                    "duration_minutes": 60,
                },
            },
            "2": {
                "summary": "Бронь №2",
                "value": {
                    "customer_name": "Бобчанский С.Л.",
                    "table_id": 2,
                    "date_from": "2025-09-01 10:00",
                    "duration_minutes": 30,
                },
            },
            "3": {
                "summary": "Бронь №3",
                "value": {
                    "customer_name": "Григорян У.В.",
                    "table_id": 5,
                    "date_from": "2025-10-01 10:20",
                    "duration_minutes": 60,
                },
            },
        }
    ),
):
    try:
        if await db.tables.get_one(id=reservations_data.table_id):
            date_to = reservations_data.date_from + timedelta(
                minutes=reservations_data.duration_minutes
            )
            date_from = reservations_data.date_from
            # Проверка на пересечение
            intersection = await db.reservations.get_filter_by_time(
                table_id=reservations_data.table_id,
                date_from=date_from,
                date_to=date_to,
            )
            if intersection:
                new_reservations_table = await db.reservations.add(reservations_data)
                await db.commit()
                return {"status": "OK", "data": new_reservations_table}
            else:
                logging.exception(
                    f"Не удалось добавить данные в БД, входные данные={reservations_data}"
                )
                raise TableIsNotAvailableHTTPException
        else:
            logging.exception(
                f"Не удалось добавить данные в БД, входные данные={reservations_data}"
            )
            raise TableNotFoundHTTPException

    except ObjectNotFoundException:
        raise TableNotFoundHTTPException


@router.delete(
    "/{reservations_id}",
    summary="Удаление",
    description="<H1>Удалить столик по id</H1>",
)
async def delete_reservations(db: DBDep, reservations_id: int):
    try:
        if await db.reservations.get_one(id=reservations_id):
            await db.reservations.remove(id=reservations_id)
            await db.commit()
            return {"status": "OK"}
    except ObjectNotFoundException:
        logging.exception(
            f"Не удалось удалить данные в БД, входные данные={reservations_id}"
        )
        raise ReservationsNotFoundHTTPException
