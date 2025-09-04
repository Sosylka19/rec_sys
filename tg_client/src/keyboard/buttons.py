from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types.keyboard_button import KeyboardButton

builder = ReplyKeyboardBuilder()
builder.add(KeyboardButton(text="Сгенерировать фильм"),
            KeyboardButton(text="Сгенерировать фильм заново"))
builder.adjust(2)