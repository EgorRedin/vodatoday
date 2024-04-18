from aiogram import Router, F
from aiogram.types import CallbackQuery
from utils.states import NewClient, OldClient
from aiogram.fsm.context import FSMContext
from keyboards.keyboards import kb_builder
import queries
from keyboards import keyboards
from queries import AsyncORM

router = Router()


@router.callback_query(F.data.in_(["new", "old"]))
async def handle_type(call: CallbackQuery, state: FSMContext):
    client = call.data
    if client == "new":
        await state.set_state(NewClient.district)
        await call.message.answer("Введите район доставки")
        await queries.AsyncORM.create_table()
    else:
        user = await AsyncORM.get_user(call.from_user.id)
        if not user:
            await call.message.answer('вас нет в базе данных')
            await call.message.answer("Здравствуйте, вы старый или новый клиент?", reply_markup=keyboards.start_kb)
            return
        await state.update_data(user=user)
        await state.set_state(OldClient.bank)
        await call.message.answer("У вас есть тара?", reply_markup=kb_builder(["Да", "Нет"], [2]))
    await call.answer()
