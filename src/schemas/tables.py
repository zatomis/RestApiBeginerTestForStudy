from pydantic import BaseModel, conint


class TablesAdd(BaseModel):
    name: str
    seats: conint(gt=0)
    location: str


class Tables(TablesAdd):
    id: int
