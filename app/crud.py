from sqlalchemy.orm import Session

from . import models, schemas

def get_user(db: Session, used_id:int):
    return db.query(models.User).filter(models.User.id == used_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = "Hashing at the front" + user.password + "Hashing at the back"
    db_user = models.User(username=user.username, password_hash=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_post(db: Session, post: schemas.CreatePost, user_id: int):
    db_post = models.Post(**post.dict(), author_id = user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post