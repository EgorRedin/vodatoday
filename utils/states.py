from aiogram.fsm.state import StatesGroup, State


class OldClient(StatesGroup):
    address = State()
    new_address = State()
    bank = State()
    payment = State()
    confirm_phone = State()
    new_phone = State()
    user = State()


class NewClient(StatesGroup):
    district = State()
    phone_number = State()
    volume = State()
    is_not_empty = State()
    payment = State()
    time = State()
    info = State()

