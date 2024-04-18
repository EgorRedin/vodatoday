from aiogram import Router
from aiogram.types import Message
from keyboards.keyboards import kb_builder
from aiogram.fsm.context import FSMContext
from utils.states import OldClient
import re
from queries import AsyncORM
from keyboards import keyboards
from aiogram import Dispatcher

router = Router()


@router.message(OldClient.bank)
async def handle_bank(msg: Message, state: FSMContext):

    if msg.text.lower() in ["да", "нет"]:
        await state.update_data(bank=(msg.text.lower() == "да"))
        await state.set_state(OldClient.payment)
        await msg.answer("Оплата наличными или картой?", reply_markup=kb_builder(["Наличные", "Карта", "Перевод"], [1]))
    else:
        await msg.answer("Я вас не понимаю, у вас есть тара?", reply_markup=kb_builder(["Да", "Нет"], [2]))


@router.message(OldClient.payment)
async def handle_payment(msg: Message, state: FSMContext):
    data = await state.get_data()
    phone_number = data['user'].phone_number
    if msg.text.lower() in ["наличные", "карта", "перевод"]:
        await state.update_data(payment=msg.text)
        await state.set_state(OldClient.confirm_phone)
        await msg.answer(f"Это ваш номер телефона - {phone_number}?", reply_markup=kb_builder(["Да", "Нет"], [2]))
    else:
        await msg.answer("Я вас не понимаю, оплата картой или наличными?", reply_markup=kb_builder(["Наличные",
                                                                                                    "Карта",
                                                                                                    "Перевод"], [1]))


@router.message(OldClient.confirm_phone)
async def handle_confirm(msg: Message, state: FSMContext):
    phone_number = 88005553535
    if msg.text.lower() in ["да", "нет"]:
        if msg.text.lower() == "да":
            await state.update_data(confirm_phone=None)
            request = await state.get_data()
            await state.clear()
            await msg.answer("Ваша заявка принята")
        else:
            await state.set_state(OldClient.new_phone)
            await msg.answer("Введите ваш номер телефона в формате - 8 999 999 99 99")
    else:
        await msg.answer(f"Я вас не понимаю, это ваш номер телефона - {phone_number}?",  reply_markup=kb_builder(["Да", "Нет"], [2]))


@router.message(OldClient.new_phone)
async def handle_new_phone(msg: Message, state: FSMContext):
    if re.search(r'^8\s9\d{2}\s\d{3}\s\d{2}\s\d{2}$', msg.text):
        await state.update_data(confirm_phone=msg.text)
        request = await state.get_data()
        await AsyncORM.update_orders(payment=request['payment'],bank = request['bank'],
                                     tg_id=msg.from_user.id,confirm_phone=request['confirm_phone'])
        await state.clear()
        await msg.answer("Ваш номер телефона обновлен")
        await msg.answer("Ваша заявка принята")
    else:
        await msg.answer("Я вас не понимаю, введите ваш номер телефона в формате - 8 999 999 99 99")

