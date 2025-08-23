from fastapi import FastAPI
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()

@app.get("/health_check")
async def health_check():
    logger.info("получен запрос db")
    print("smth db")
    return {"status": "Db service started"}