from typing import Annotated

from database_init import Base, str_255
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, BigInteger
import enum

intpk = Annotated[int, mapped_column(autoincrement=True, primary_key=True)]

class User(Base):
    __tablename__ = "users"
    id: Mapped[intpk]
    tg_id = mapped_column(BigInteger)
    phone_number: Mapped[str]
    orders: Mapped[list["Order"]] = relationship(back_populates="user")


    def __repr__(self):
        return f'golova: {self.tg_id},{self.orders}'

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[intpk]
    count: Mapped[int] = mapped_column(nullable=True)
    address: Mapped[str]
    payment: Mapped[str]
    time_del: Mapped[str]
    bank: Mapped[bool]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    info: Mapped[str_255] = mapped_column(nullable=True)
    user: Mapped["User"] = relationship(back_populates="orders")
    def __repr__(self):
        return f'greben:  {self.id},{self.address}'
