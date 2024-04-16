from aiogram import Router, F
from aiogram.types import Message
from keyboards.keyboards import kb_builder
from aiogram.fsm.context import FSMContext
from utils.states import NewClient
import re
from main import db

router = Router()


@router.message(NewClient.district)
async def handle_district(msg: Message, state: FSMContext):
    await state.update_data(district=msg.text)
    await state.set_state(NewClient.volume)
    await msg.answer("Введите объем")


@router.message(NewClient.volume)
async def handle_volume(msg: Message, state: FSMContext):
    if re.search(r'\d', msg.text):
        await state.update_data(volume=int(msg.text))
        await state.set_state(NewClient.is_not_empty)
        await msg.answer("У вас есть пустая тара?", reply_markup=kb_builder(["Да", "Нет"], [2]))
    else:
        await msg.answer("Введите просто число")


@router.message(NewClient.is_not_empty)
async def handle_empty(msg: Message, state: FSMContext):
    if msg.text.lower() not in ["да", "нет"]:
        await msg.answer("Я вас не понимаю, у вас есть пустая тара?", reply_markup=kb_builder(["Да", "Нет"], [2]))
    else:
        await state.update_data(is_not_empty=(msg.text.lower() == "да"))
        await state.set_state(NewClient.payment)
        await msg.answer("Оплата наличными или картой?", reply_markup=kb_builder(["Наличные", "Карта"], [1]))


@router.message(NewClient.payment)
async def handle_payment(msg: Message, state: FSMContext):
    if msg.text.lower() not in ["наличные", "карта"]:
        await msg.answer("Я вас не понимаю, оплата наличными или картой?", reply_markup=kb_builder(["Наличные", "Карта"], [1]))
    else:
        await state.update_data(payment=msg.text.lower())
        await state.set_state(NewClient.phone_number)
        await msg.answer("Введите свой номер телефона - в формате в формате  7 999 999 99 99")


@router.message(NewClient.phone_number)
async def handle_number(msg: Message, state: FSMContext):
    if re.search(r'^7\s9\d{2}\s\d{3}\s\d{2}\s\d{2}$', msg.text):
        await state.update_data(phone_number=msg.text)
        request = await state.get_data()
        print(request)
        request.update({"id": msg.from_user.id})
        db.append(request)
        await state.clear()
        await msg.answer("Ваша заявка отправлена")
