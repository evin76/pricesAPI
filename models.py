from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Numeric
from sqlalchemy.orm import relationship

from database import Base


class Price(Base):
    __tablename__ = "price"
    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime)
    name = Column(String(64))
    price = Column(String(64))
    price_int = Column(Numeric(10, 2))
    url = Column(String(64))

    def __repr__(self):
        return f"{self.name} | {self.price}"
