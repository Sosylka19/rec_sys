from typing import List
from ml_kernel import recommend_movies
class Recommender():
    def __init__(self, film: str):
        self.film = film

    def recommend(self, recommendation: List[str]) -> str:
        return ", ".join(recommend_movies(self.film))