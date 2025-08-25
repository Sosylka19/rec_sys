from pydantic import BaseModel
from typing import List

class CreateHistory(BaseModel):
    session_id: str
    film: str
    recommendation: str


class GetHistory(BaseModel):
    session_id: str