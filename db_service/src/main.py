from fastapi import FastAPI, HTTPException, Depends
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, select
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.db import init_db, get_session
from app.models import Logs


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
async def add_history():
    logger.info("DB've got request")
    return {"status": "Db service started"}