from aiogram import Router
from aiogram.types import Message
from keyboards.keyboards import kb_builder
from aiogram.fsm.context import FSMContext
from utils.states import NewClient
import re
from queries import AsyncORM


router = Router()

@router.message(NewClient.district)
async def handle_district(msg: Message, state: FSMContext):
    await state.update_data(district=msg.text)
    await state.set_state(NewClient.phone_number)
    await msg.answer("Введите номер телефона в формате - 8 999 999 99 99")


@router.message(NewClient.phone_number)
async def handle_phone(msg: Message, state: FSMContext):
    if re.search(r'^8\s9\d{2}\s\d{3}\s\d{2}\s\d{2}$', msg.text):
        await state.update_data(phone_number=msg.text)
        await state.set_state(NewClient.volume)
        await msg.answer("Сколько бутылей воды тм Vodatoday 19л желаете заказать?")
    else:
        await msg.answer("Я вас не понимаю, введите номер телефона в формате - 8 999 999 99 99")


@router.message(NewClient.volume)
async def handle_volume(msg: Message, state: FSMContext):
    if re.search(r'\d', msg.text):
        await state.update_data(volume=int(msg.text))
        await state.set_state(NewClient.is_not_empty)
        await msg.answer("Будет ли пустая тара взамен привезенных?", reply_markup=kb_builder(["Да", "Нет"], [2]))
    else:
        await msg.answer("Введите просто число")


@router.message(NewClient.is_not_empty)
async def handle_empty(msg: Message, state: FSMContext):
    if msg.text.lower() not in ["да", "нет"]:
        await msg.answer("Я вас не понимаю, у вас есть пустая тара?", reply_markup=kb_builder(["Да", "Нет"], [2]))
    else:
        await state.update_data(is_not_empty=(msg.text.lower() == "да"))
        await state.set_state(NewClient.payment)
        await msg.answer("Оплата нал/безнал/перевод на карту?", reply_markup=kb_builder(["Наличные", "Карта",
                                                                                         "Перевод"],
                                                                                        [1]))


@router.message(NewClient.payment)
async def handle_payment(msg: Message, state: FSMContext):
    if msg.text.lower() not in ["наличные", "карта", "перевод"]:
        await msg.answer("Я вас не понимаю, оплата нал/безнал/перевод на карту??", reply_markup=kb_builder([
            "Наличные", "Карта", "Перевод"], [1]))
    else:
        await state.update_data(payment=msg.text.lower())
        await state.set_state(NewClient.time)
        await msg.answer("Время доставки с 9-12 или 12-18?", reply_markup=kb_builder(["9-12", "12-18"], [1]))


@router.message(NewClient.time)
async def handle_time(msg: Message, state: FSMContext):
    if msg.text.lower() in ["9-12", "12-18"]:
        await state.update_data(time=msg.text)
        await state.set_state(NewClient.info)
        await msg.answer("Введите доп. информацию (максимум 255 символов, остальные будут проигнорированы), "
                         "если не хотите напишите \"Нет\"")
    else:
        await msg.answer("Я вас не понимаю, время доставки с 9-12 или 12-18?", reply_markup=kb_builder(["9-12", "12-18"], [1]))


@router.message(NewClient.info)
async def handle_info(msg: Message, state: FSMContext):
    if msg.text.lower() == "нет":
        request = await state.get_data()
        await AsyncORM.insert_users(count=request['volume'], address=request['district'],
                                    phone_number=request['phone_number'], payment=request['payment'],
                                    time_del=request['time'], bank=request['is_not_empty'], info=None,
                                    tg_id=msg.from_user.id)
        await state.clear()
        await msg.answer("Ваша заявка принята")
    else:
        await state.update_data(info=msg.text[:256:])
        request = await state.get_data()
        await AsyncORM.insert_users(count=request['volume'],address=request['district'],
                                    phone_number=request['phone_number'], payment=request['payment'],
                                    time_del=request['time'], bank=request['is_not_empty'], info=request['info'],
                                    tg_id=msg.from_user.id)
        await state.clear()
        await msg.answer("Ваша заявка принята")
