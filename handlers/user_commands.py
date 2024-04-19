from aiogram.filters import CommandStart
from aiogram import Router
from aiogram.types import Message
import queries
from keyboards import keyboards

router = Router()


@router.message(CommandStart())
async def start_cmd(msg: Message):
    await queries.AsyncORM.create_table()
    await msg.answer("Здравствуйте, вы старый или новый клиент?", reply_markup=keyboards.start_kb)

