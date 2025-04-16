# ruff : noqa: E402
# спец файл для того чтобы при каждом прогоне
# тестов выполнялся. Файл настроечный - основной настроечный
from typing import AsyncGenerator
from unittest import mock

from src.schemas.tables import TablesAdd

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import json
from pprint import pprint

import pytest

from src.api.dependencies import get_db
from src.config import settings
from src.database import (
    BaseModelORM,
    engine_null_pull,
    new_async_session_maker_null_pool,
)
from src.main import app
from src.models import *  # noqa
from httpx import AsyncClient

from src.schemas.tables import TablesAdd  # noqa F811
from src.utils.db_manager import DBManager


# фикстура, которая вернет подключение в БД
@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=new_async_session_maker_null_pool) as db:
        yield db


async def get_db_null_pull() -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=new_async_session_maker_null_pool) as db:
        pprint("Перезаписан метод работы с БД")
        yield db


# для тестов чтобы не было ошибок-необходимо подменить обращение к БД
# это необходимо для теста, который делает API запрос
# и там достаточно "пустого" подключения. Ниже через метод подменяем на новую функцию
app.dependency_overrides[get_db] = get_db_null_pull


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"


# автоматически запустить эту функцию но только для сессии т.е. один раз
# т.к. в самом начале тестов прогоняется именно этот файл - первым
# где удаляются и создаются тестовые таблицы
@pytest.fixture(scope="session", autouse=True)
async def setup_DB_main(check_test_mode):
    print("ФИКСТУРА")
    async with engine_null_pull.begin() as conn:
        await conn.run_sync(BaseModelORM.metadata.drop_all)
        await conn.run_sync(BaseModelORM.metadata.create_all)

    with open("tests/tables.json", encoding="utf-8") as tables_test:
        tables_data = json.load(tables_test)

    tables = [TablesAdd.model_validate(table) for table in tables_data]

    async with DBManager(session_factory=new_async_session_maker_null_pool) as db_:
        print("Создание тестовых данных")
        await db_.tables.add_bulk(tables)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://testuser") as ac:
        yield ac
