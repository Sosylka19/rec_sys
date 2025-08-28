from fastapi import FastAPI, Body
from typing import Union, List

from recommender.recommender import Recommender

app = FastAPI()

@app.post("/recommend/")
async def health_check(film: str = Body(...), recommendation: List[str] = Body(...)):
    """
    Form a response to a film recommendation request.
    """

    answer = Recommender(film).recommend(recommendation=recommendation)

    return {
        "status code": "ok",
        "recommendation": answer
    }