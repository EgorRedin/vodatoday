from database_init import engine, Base, session_factory
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models import User, Order


class AsyncORM:

    @staticmethod
    async def create_table():
        async with engine.begin() as conn:
            #await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def insert_users(count: int, address: str, payment: str, time_del: str, bank: bool, info: str | None,
                           tg_id: int, phone_number: str):
        async with session_factory() as session:
            order = Order(count=count, address = address, payment=payment, time_del=time_del, bank=bank, info=info)
            user = User(tg_id=tg_id, phone_number=phone_number, orders=[order])
            session.add_all([user, order])
            await session.commit()

    @staticmethod
    async def update_orders(payment: str, bank: bool, tg_id: int, address: str, count=0, confirm_phone=None):
        async with session_factory() as session:
            query = (select(User).where(User.tg_id == tg_id).options(selectinload(User.orders)))
            res = await session.execute(query)
            result = res.scalars().one()
            new_order = Order(payment=payment, bank=bank, address=address,
                              time_del=result.orders[0].time_del, count=count)
            result.orders.append(new_order)
            if confirm_phone:
                result.phone_number = confirm_phone
            await session.commit()

    @staticmethod
    async def get_user(tg_id: int):
        async with session_factory() as session:
            query = select(User).where(User.tg_id == tg_id).options(selectinload(User.orders))
            res = await session.execute(query)
            result = res.scalars().first()
        return result







