from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from .database import sessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/")
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db,skip,limit)
    return users

@app.post("/users/")
async def create_users(user: schemas.UserCreate,db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db,user.username)
    if db_user:
        raise HTTPException(status_code = 404, detail = "Username already exists")
    return crud.create_user(db=db,user=user)