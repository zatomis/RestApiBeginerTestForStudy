from pprint import pprint
from src.schemas.tables import TablesAdd
from src.utils.db_manager import DBManager


# тут передаем фикстуру, которая делает подключение к БД
# и тогда функция ниже - уже будет внутри контекстного менеджера
async def test_add_tabel(db: DBManager):
    table_data = TablesAdd(name="Столик 1", seats=2, location="Столик у окна")
    new_table = await db.tables.add(table_data)
    pprint(f"f{new_table=}")
    await db.commit()
    assert new_table.id == 5  # т.к. 4 из тестового файла
