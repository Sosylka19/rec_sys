from aiogram import Router, F 
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import requests

from keyboard.buttons import builder

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
    ###
    #Call ml_service
    def call_ml_service(): pass
    film_recommendations = "Titanic, Formulae 1"
    ###
    data_post = {
        "session_id": f"{session_id}",
       "film": f"{film}",
       "recommendation": f"{film_recommendations}"
    }  


    try:
        r = requests.post(url='http://localhost/recommender/db', json=data_post)

        if r.status_code == 200:
            text = f"Your recommendation: {film_recommendations}"
        elif r.status_code == 404:
            text = "Sorry, session ID not found"
        elif r.status_code == 500:
            text = "Sorry, database error"
        elif r.status_code == 422:
            try:
                error_data = r.json()
                text = f"Validation Error: {error_data}"
            except ValueError:
                text = "Validation Error: Unable to parse error details" 
        else:
            r.raise_for_status()

    except requests.exceptions.RequestException as err:
        text = f"Sorry, failed, err: {err.args[0]}"

    await message.answer(
        text
    )

@start_router.message(F.text.lower() == "regenerate recommendation")
async def cmd_regenerate(message: Message, state: FSMContext):
    user_data = await state.get_data()
    film = user_data.get('last_film')
    session_id = user_data.get('session_id')
    data_regenerate = {
        "session_id": str(session_id)
    }

    if not film:
        await message.answer("Input film with 'Generate film' ")
        return
    
    try:
        r = requests.get(url='http://localhost/recommender/db', json=data_regenerate)

        if r.status_code == 200:
            recommended_films = [i[1] for i in (r.json())["recommendation"]]

            #call model again with list
            def call_model(): pass
            film_recommendation = []

            text = " ".join(recommended_films)
            # text = "GET request works fine"
            
        elif r.status_code == 404:
            text = "Sorry, session ID not found"
        elif r.status_code == 500:
            text = "Sorry, database error"
        elif r.status_code == 422:
            try:
                error_data = r.json()
                text = f"Validation Error: {error_data}"
            except ValueError:
                text = "Validation Error: Unable to parse error details" 
        else:
            r.raise_for_status()

    except requests.exceptions.RequestException as err:
        text = f"Sorry, failed, err: {err.args[0]}"


    await message.answer(
        text
    )

    
