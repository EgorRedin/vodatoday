from aiogram import Router, F
from aiogram.types import Message
from keyboards.keyboards import kb_builder
from aiogram.fsm.context import FSMContext
from utils.states import OldClient
import re
from main import db

router = Router()


@router.message(OldClient.bank)
async def handle_district(msg: Message, state: FSMContext):
    if msg.text.lower() in ["да", "нет"]:
        await state.update_data(bank=(msg.text.lower() == "да"))
        await state.set_state(OldClient.payment)
        await msg.answer("Оплата наличными или картой?", reply_markup=kb_builder(["Наличные", "Карта"], [1]))
    else:
        await msg.answer("Я вас не понимаю, у вас есть тара?", reply_markup=kb_builder(["Да", "Нет"], [2]))


@router.message(OldClient.payment)
async def handle_payment(msg: Message, state: FSMContext):
    phone_number = "89447861232"  # тут по идеи берем из БД, но пока нет, так
    if msg.text.lower() in ["наличные", "карта"]:
        await state.update_data(payment=msg.text)
        await state.set_state(OldClient.confirm_phone)
        await msg.answer(f"Это ваш номер телефона - {phone_number}?", reply_markup=kb_builder(["Да", "Нет"], [2]))
    else:
        await msg.answer("Я вас не понимаю, оплата картой или наличными?", reply_markup=kb_builder(["Наличные", "Карта"], [1]))


#Тут надо дописать, чтобы по нормальному было

@router.message(OldClient.confirm_phone)
async def handle_confirm(msg: Message, state: FSMContext):
    phone_number = 71923812117
    if msg.text.lower() not in ["да", "нет"]:
        await msg.answer("Пожалуйста, ответьте 'да' или 'нет'.")
    else:
        if msg.text.lower() == "да":
            await state.update_data(confirm_phone="3892382392") # тут тоже без бд
            request = await state.get_data()
            request.update({"id": msg.from_user.id})
            db.append(request)
            await state.clear()
            await msg.answer("Ваша заявка принята")
        else:
            await state.set_state(OldClient.confirm_phone2)
            await msg.answer("Введите ваш актуальный номер телефона")
            await state.update_data(confirm_phone=False)

@router.message(OldClient.confirm_phone2)
async def handle_confirm_number(msg: Message, state: FSMContext):
    phone_number = 71923812117
    if re.search(r'^7\s9\d{2}\s\d{3}\s\d{2}\s\d{2}$', msg.text):
        await state.update_data(confirm_phone=msg.text)
        request = await state.get_data()
        request.update({"id": msg.from_user.id})
        db.append(request)
        await state.clear()
        await msg.answer("Ваш номер телефона изменен")
        await msg.answer("Ваша завяка принята")
    else:
        await msg.answer('Введите номер телефона в формате 7 999 999 99 99')
