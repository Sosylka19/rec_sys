from sqlmodel import Field, SQLModel

class History(SQLModel, table=True):
    """
    Register history & logs of client's queries
    """
    id: int | None = Field(default=None, primary_key=True)
    session_id: str
    timestamp: str
    question: str
    answer: str

