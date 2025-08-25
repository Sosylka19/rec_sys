from aiogram import Router, F 
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import requests

start_router = Router()

class Form(StatesGroup):
    name = State()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Welcome! This is a bot that helps you with finding suitable films. "
        "Use /help to see available commands."
    )

@start_router.message(Command('film'))
async def cmd_recommender(message: Message, state: FSMContext):

    await state.set_state(Form.name)
    await message.answer(
        "Введи название фильма: "
    )

@start_router.message()
async def process_film(message: Message, state: FSMContext):
    session_id = message.message_id
    film = message.text
    if not film:
        raise ValueError("There is not input film")
    ###
    #Call ml_service
    def call_ml_service(): pass
    film_recommendations = "Titanic, Formulae 1"
    ###
    data_post = {
        "session_id": f"{session_id}",
       "film": f"{film}",
       "recommenation": f"{film_recommendations}"
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

# @start_router.message(Command('regenerate'))
# async def cmd_regenerate(message: Message):
#     session_id = 0 #Trash
#     film = 'bla' #Last film
#     data_regenerate = {
#         "session_id": str(session_id),
#         "film": str(film)
#     }
#     try:
#         request = requests.get(url='http://localhost/recommender/db', json=data_regenerate) # Get pull of the recommended earlier films
#     except:
#         raise ValueError("Bad request")
    
#     recommended_films = [i[1] for i in (request.json())["question_answer"]]

#     #call model again with list

#     film_recommendation = []
#     if film_recommendation:
#         text = " ".join(film_recommendation)
#     else:
#         text = "Sorry, bad request from server"


#     await message.answer(
#         text
#     )

    
