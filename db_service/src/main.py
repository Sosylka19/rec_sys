from fastapi import FastAPI, HTTPException, Depends, status, Body
from contextlib import asynccontextmanager
from sqlmodel import Session, select
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from db import init_db, get_session
from models import History
from schemas import CreateHistory, GetHistory


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
    try:

        new_record = History(
            session_id=history.session_id,
            film=history.film,
            recommendation=history.recommendation
        )

        session.add(new_record)
        session.commit()
        session.refresh(new_record)

        return {
            "status": "ok",
            "session_id": new_record.session_id
        }
    except SQLAlchemyError as err:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(err)}"
        )

@app.get("/history/")
async def get_history(
    history: GetHistory, session: Session = Depends(get_session)
    ):
    
    statement = select(History).where(History.session_id == history.session_id)
    #check if it works
    results = session.exec(statement).all()

    if not results:
        raise HTTPException(status_code=404, detail="Session ID not found")

    recommendation = [[record.film, record.recommendation] for record in results]

    return {"recommendation": recommendation}