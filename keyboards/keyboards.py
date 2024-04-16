from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

start_kb = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Новый клиент", callback_data="new")
        ],
        [
            InlineKeyboardButton(text="Старый клиент", callback_data="old")
        ]
    ]
)


def kb_builder(buttons: list, grid: list):
    builder = ReplyKeyboardBuilder()
    for button in buttons:
        builder.button(text=button)
    builder.adjust(*grid)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True, selective=True)
