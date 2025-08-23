from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Welcome! This is a bot that helps you with various tasks. "
        "Use /help to see available commands."
    )
# Здесь будет обрабатываться фильм пользователя и отправляться будут get запрос к мл_сервису и для логов в бд
@start_router.message(Command('start_2'))
async def cmd_start_2(message: Message):
    await message.answer(
        "This is another start command. Use /help to see available commands."
    )

