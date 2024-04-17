from typing import Annotated

from database_init import Base, str_255
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, BigInteger
import enum

intpk = Annotated[int, mapped_column(autoincrement=True, primary_key=True)]


class Payment(enum.Enum):
    cash = "Наличные"
    card = "Карта"
    transaction = "Перевод"


class Time(enum.Enum):
    first_part = "9-12"
    second_part = "12-18"


class User(Base):
    __tablename__ = "users"
    id: Mapped[intpk]
    tg_id = mapped_column(BigInteger)
    phone_number: Mapped[str]
    orders: Mapped[list["Order"]] = relationship()


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[intpk]
    count: Mapped[int]
    address: Mapped[str]
    payment: Mapped[Payment]
    time: Mapped[Time]
    bank: Mapped[bool]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    info: Mapped[str_255]
    user: Mapped["User"] = relationship()
