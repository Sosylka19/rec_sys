from aiogram import Router, F 
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.methods.send_media_group import SendMediaGroup
import requests

from keyboard.buttons import builder
from handlers.ml_request import generate_films, regenerate_films

start_router = Router()

class Form(StatesGroup):
    name = State()

@start_router.message(CommandStart())
async def cmd_start(message: Message):

    await message.answer(
        "Welcome! This is a bot that helps you with finding suitable films. "
        "Use /help to see available commands.",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )

@start_router.message(F.text.lower() == "generate film")
async def cmd_recommender(message: Message, state: FSMContext):

    await state.set_state(Form.name)
    await message.answer(
        "Введи название фильма: "
    )

@start_router.message(Form.name)
async def process_film(message: Message, state: FSMContext):
    session_id = message.message_id
    film = message.text
    if not film:
        await message.answer("Please input film")
        return
    
    await state.update_data(last_film=film, session_id=session_id)
    await state.set_state(None)

    text = generate_films(session_id=str(session_id), film=film, recommendation=[""]) # dict {text, info} - format
    if text['text'] == "Success":
        dict_values = text['info'] #List of 5 descriptions

        media_group = MediaGroupBuilder()
        for i in range(5):
            if dict_values[i]['poster_url'] != "no":
                media_group.add_photo(media=dict_values[i]['poster_url'])

        await message.reply_media_group(
            media=media_group.build()
        )
    else:
        await message.answer(
            text["text"]
        )
 

@start_router.message(F.text.lower() == "regenerate recommendation")
async def cmd_regenerate(message: Message, state: FSMContext):
    user_data = await state.get_data()
    film = user_data.get('last_film')
    session_id = user_data.get('session_id')

    if not film:
        await message.answer("Input film with 'Generate film' ")
        return
    
    text = regenerate_films(session_id=str(session_id), film=film)

    if text['text'] == "Success":
        dict_values = text['info'] #List of 5 descriptions

        media_group = MediaGroupBuilder()
        for i in range(5):
            media_group.add_photo(media=dict_values[i]['poster_url'])

        await message.reply_media_group(
            media=media_group.build()
        )
    else:
        await message.answer(
            text["text"]
        )
    


    
