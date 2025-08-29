from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types.keyboard_button import KeyboardButton

builder = ReplyKeyboardBuilder()
builder.add(KeyboardButton(text="Generate film"),
            KeyboardButton(text="Regenerate recommendation"))
builder.adjust(2)