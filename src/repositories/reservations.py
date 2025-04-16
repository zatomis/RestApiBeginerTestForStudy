from src.models.reservations import ReservationsORM
from src.repositories.base import BaseRepository
from src.repositories.utils import check_for_reserv
from src.schemas.reservations import Reservation


class ReservationsRepository(BaseRepository):
    model = ReservationsORM
    schema = Reservation

    async def get_filter_by_time(self, table_id, date_from, date_to):
        table_id_to_get = check_for_reserv(date_from, date_to, table_id)
        query_result = await self.session.execute(table_id_to_get)
        if not query_result.scalars().all():
            return True  #      т.е. нет пересечений - можно добавить
        else:
            return False
