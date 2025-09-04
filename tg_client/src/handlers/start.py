from aiogram import Router, F 
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import html
from translate import Translator

from keyboard.buttons import builder
from handlers.ml_request import generate_films, regenerate_films

start_router = Router()

class Form(StatesGroup):
    name = State()

@start_router.message(CommandStart())
async def cmd_start(message: Message):

    await message.answer_photo(
        photo="https://upload.wikimedia.org/wikipedia/en/e/e6/AI_Poster.jpg")
    await message.answer(
        "Привет, этот бот помогает искать фильмы, похожие на тот, который ты введешь.\nНажми на кнопку 'Сгенерировать фильм', чтобы начать!\n" \
        "P.S На Английском языке фильмы ищутся лучше:)",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )

@start_router.message(F.text.lower() == "сгенерировать фильм")
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
        await message.answer("Введите фильм")
        return
    
    await state.update_data(last_film=film, session_id=session_id)
    await state.set_state(None)

    translate = Translator(from_lang='russian', to_lang='english')
    film = translate.translate(film)
    film = film.title()

    text = generate_films(session_id=str(session_id), film=film, recommendation=[""]) # dict {text, info} - format
    if text['text'] == "Success":
        dict_values = text['info'] #List of 5 descriptions

        for i in range(5): 
            await message.answer_photo(
                photo=dict_values[i]['poster_url'],
                caption = f"<b>{html.escape(dict_values[i]['title'])}</b>\n\nОценка: {dict_values[i]['rating']}\n\nОписание:\n{html.escape(dict_values[i]['overview'])}"
                )
    else:
        await message.answer(
            text["text"]
        )
 

@start_router.message(F.text.lower() == "сгенерировать фильм заново")
async def cmd_regenerate(message: Message, state: FSMContext):
    user_data = await state.get_data()
    film = str(user_data.get('last_film'))

    translate = Translator(from_lang='russian', to_lang='english')
    film = translate.translate(film)
    film = film.title()

    session_id = user_data.get('session_id')

    if not film:
        await message.answer("Введите фильм при помощи 'Сгенерировать фильм' ")
        return
    
    text = regenerate_films(session_id=str(session_id), film=film)

    if text['text'] == "Success":
        dict_values = text['info'] #List of 5 descriptions

        for i in range(5): 
            await message.answer_photo(
                photo=dict_values[i]['poster_url'],
                caption = f"<b>{html.escape(dict_values[i]['title'])}</b>\n\nОценка: {dict_values[i]['rating']}\n\nОписание:\n{html.escape(dict_values[i]['overview'])}"
                )
    else:
        await message.answer(
            text["text"]
        )
    


    
