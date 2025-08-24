from fastapi import FastAPI, HTTPException, Depends
from contextlib import asynccontextmanager
from sqlmodel import Session, select
from fastapi.middleware.cors import CORSMiddleware
import logging

from db import init_db, get_session
from models import History
from schemas import CreateHistory, GetHistory


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/history/")
async def add_history(history: CreateHistory, session: Session = Depends(get_session)):

    logger.info("DB've got request")

    new_record = History(
        session_id=history.session_id,
        timestamp=history.timestamp,
        question=history.question,
        answer=history.answer
    )

    session.add(new_record)
    session.commit()
    session.refresh(new_record)

    return {"status": "Db service started"}

@app.get("/history/")
async def get_history(history: CreateHistory, session: Session = Depends(get_session)):
    logger.info("DB've sent request")

    statement = select(History).where(History.session_id == history.session_id)
    results = session.exec(statement).all()

    if not results:
        raise HTTPException(status_code=404, detail="Session ID not found")

    timestamps = [record.timestamp for record in results]
    question_answer = [[record.question, record.answer] for record in results]

    return GetHistory(
        session_id=history.session_id,
        timestamp=timestamps,
        question_answer=question_answer
    )