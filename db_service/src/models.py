from sqlmodel import Field, SQLModel

class History(SQLModel, table=True):
    """
    Register history & logs of client's queries
    """
    session_id: str = Field(default=None)
    timestamp: str = Field(default=None)
    question: str = Field(default=None)
    answer: str = Field(default=None)

