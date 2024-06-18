from typing import List, Union
from datetime import datetime
from pydantic import BaseModel

class PriceBase(BaseModel):
    name: str
    url: str = None
    price: str
    price_int: int


class PriceCreate(PriceBase):
    #datetime: str
    pass

class Price(PriceBase):
    id: int
    datetime: datetime

    class Config:
        orm_mode = True
