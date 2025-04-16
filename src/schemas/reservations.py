from datetime import datetime

from pydantic import BaseModel, conint, constr


class ReservationAdd(BaseModel):
    customer_name: constr(min_length=3)
    table_id: int
    date_from: datetime
    duration_minutes: conint(gt=0)


class Reservation(ReservationAdd):
    id: int
