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
    user = await AsyncORM.get_user(call.from_user.id)
    if client == "new":
        if user:
            await call.message.answer("Вы уже есть в базе данных, авторизуйтесь как старый клиент")
            await call.message.answer("Здравствуйте, вы старый или новый клиент?", reply_markup=keyboards.start_kb)
            await call.answer()
            return
        await state.set_state(NewClient.district)
        await call.message.answer("Введите район доставки (улица, номер дома, квартира)")
    else:
        if not user:
            await call.message.answer('Вас нет в базе данных, авторизуйтесь как новый клиент')
            await call.message.answer("Здравствуйте, вы старый или новый клиент?", reply_markup=keyboards.start_kb)
            await call.answer()
            return
        await state.update_data(user=user)
        await state.set_state(OldClient.address)
        addresses = list(set([order.address for order in user.orders][::-1])) + ["Новый адрес"]
        await state.update_data(address=addresses)
        await call.message.answer("Выберите адрес доставки", reply_markup=keyboards.kb_builder(addresses, [1]))
    await call.answer()
