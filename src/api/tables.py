from fastapi import APIRouter, Body
from src.api.dependencies import DBDep
from src.exceptions import ObjectNotFoundException, TableNotFoundHTTPException
from src.schemas.tables import TablesAdd

router = APIRouter(prefix="/tables", tags=["Столики 🍱"])


@router.get("/")
async def get_tables(db: DBDep):
    tables = await db.tables.get_all()
    return {"data": tables}


@router.post("/", summary="Добавить данные", description="<H1>Бронирование</H1>")
async def create_table(
    db: DBDep,
    table_data: TablesAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Столик №1",
                "value": {"name": "Table 1", "seats": 5, "location": "Зал у окна"},
            },
            "2": {
                "summary": "Столик №2",
                "value": {"name": "Table 2", "seats": 4, "location": "Напрoтив Бара"},
            },
            "3": {
                "summary": "Столик №3",
                "value": {"name": "Table 3", "seats": "2", "location": "Терасса"},
            },
        }
    ),
):
    table = await db.tables.add(table_data)
    await db.commit()
    return {"status": "OK", "data": table}


@router.delete(
    "/{table_id}", summary="Удаление", description="<H1>Удалить столик по id</H1>"
)
async def delete_table(db: DBDep, table_id: int):
    try:
        if await db.tables.get_one(id=table_id):
            await db.tables.remove(id=table_id)
            await db.commit()
            return {"status": "OK"}
    except ObjectNotFoundException:
        raise TableNotFoundHTTPException
