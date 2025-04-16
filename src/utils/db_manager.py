# для того чтобы уйти от контекстных менеджеров и сделать свой
from src.repositories.reservations import ReservationsRepository
from src.repositories.tables import TablesRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.tables = TablesRepository(self.session)
        self.reservations = ReservationsRepository(self.session)
        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
