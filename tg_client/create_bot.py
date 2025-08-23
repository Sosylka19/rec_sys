import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os

# from db_handler.db_class import PostgresHandler

# pg_db = PostgresHandler(config('PG_LINK'))
load_dotenv()

token = os.getenv('TOKEN')
if not token:
    raise ValueError("TOKEN environment variable is not set.")
scheduler = AsyncIOScheduler(timezone='Europe/Moscow')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

bot = Bot(
    token=token,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML)

)

dp = Dispatcher(
    storage=MemoryStorage()
)