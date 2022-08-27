from datetime import datetime
from gettext import dpgettext
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import crud, models, schemas
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from .database import sessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def fake_hash_password(password: str):
    return "Hashing at the front" + password + "Hashing at the back"

def fake_decode_token(token):
    user = crud.get_user_by_username(db=db,username=username)

def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect Username or Password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user

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

@app.get("/posts/")
async def read_all_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud.get_all_posts(db,skip,limit)
    return posts

@app.post("/posts/{user_id}/post")
async def make_post(user_id: int, post: schemas.CreatePost,db: Session = Depends(get_db)):
    return crud.create_post(db=db,post=post,user_id=user_id)

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_dict = crud.get_user_by_username(db=db, username=form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, 
        detail="Incorrect Username or Password")
    user = user_dict.username
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user_dict.password_hash:
        raise HTTPException(status_code=400,
        detail="Incorrect Username or Password")

    return {"access_token": user , "token_type":"bearer"}