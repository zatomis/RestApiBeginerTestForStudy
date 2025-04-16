from src.models.tables import TablesORM
from src.repositories.base import BaseRepository
from src.schemas.tables import Tables


class TablesRepository(BaseRepository):
    model = TablesORM
    schema = Tables
