from aiogram.filters import CommandStart
from aiogram import Router, F
from aiogram.types import Message
from keyboards import keyboards

router = Router()


@router.message(CommandStart())
async def start_cmd(msg: Message):
    await msg.answer("Здравствуйте, вы старый или новый клиент?", reply_markup=keyboards.start_kb)

