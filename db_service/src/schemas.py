from pydantic import BaseModel
from typing import List, Union

class CreateHistory(BaseModel):
    session_id: str
    timestamp: str
    question: str
    answer: str


class GetHistory(BaseModel):
    session_id: str
    timestamp: List[str]
    question_answer: List[List[str]]  # List of [question, answer] pairs