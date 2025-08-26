from fastapi import FastAPI
from typing import Union, List

from recommender.recommender import Recommender

app = FastAPI()

@app.get("/recommend/")
async def health_check(film: str, recommendation: List[str]):
    """
    Form a response to a film recommendation request.
    """

    answer = Recommender(film).recommend(recommendation=recommendation)

    return {
        "status code": "ok",
        "recommendation": answer
    }