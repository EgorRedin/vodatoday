from aiogram import Router, F
from aiogram.types import CallbackQuery
from utils.states import NewClient, OldClient
from aiogram.fsm.context import FSMContext
from keyboards.keyboards import kb_builder
from DB import queries

router = Router()


@router.callback_query(F.data.in_(["new", "old"]))
async def handle_type(call: CallbackQuery, state: FSMContext):
    client = call.data
    if client == "new":
        await state.set_state(NewClient.district)
        await call.message.answer("Введите район доставки")
        await queries.AsyncORM.create_table()
    else:
        await state.set_state(OldClient.bank)
        await call.message.answer("У вас есть тара?", reply_markup=kb_builder(["Да", "Нет"], [2]))
    await call.answer()
