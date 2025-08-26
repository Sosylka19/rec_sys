from fastapi import FastAPI
from typing import Union, List

from recommender.recommender import Recommender

app = FastAPI()

@app.get("/recommend/")
async def health_check(film: str, recommendation: Union[List[List[str]], None]):
    """
    Form a response to a film recommendation request.
    """
    if not recommendation:
        recommendation = []
        
    answer = Recommender(film).recommend(recommendation=recommendation)

    return {
        "status code": "ok",
        "recommendation": answer
    }