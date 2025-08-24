from fastapi import FastAPI
import logging



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()

@app.get("/recommend/")
async def health_check():
    """
    Form a response to a film recommendation request.
    """
    logger.info("ML've recieved a request")
    return {"status": "ml-service service started"}