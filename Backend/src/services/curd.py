from sqlalchemy.orm import Session

from Backend.src.services import model, schema
# from . import models,schemas



#NOTE: we will use it to get all users
def get_users(db: Session, skip:int=0, limit:int=100):
    return db.query(model.User).offset(skip).limit(limit).all()

#NOTE: we will use it tot get user by id
def get_user(db: Session, user_name: str ,user_id: int):
    user_exists = db.query(model.User).filter(model.User.name == user_name).first()
    # if user_exists #TODO: need to implement hash password
    return db.query(model.User).filter(model.User.name == user_name).first()