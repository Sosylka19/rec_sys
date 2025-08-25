from fastapi import FastAPI

app = FastAPI()

@app.get("/recommend/")
async def health_check():
    """
    Form a response to a film recommendation request.
    """
    return {"status": "ml-service service started"}