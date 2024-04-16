from aiogram.fsm.state import StatesGroup, State


class OldClient(StatesGroup):
    bank = State()
    payment = State()
    confirm_phone = State()
    confirm_phone2 = State()


class NewClient(StatesGroup):
    district = State()
    volume = State()
    is_not_empty = State()
    payment = State()
    phone_number = State()
