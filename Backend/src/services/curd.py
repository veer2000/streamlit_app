from sqlalchemy.orm import Session

from ..services import model, schema
import inspect


func_name = inspect.currentframe().f_code.co_name

#NOTE: we will use it to get all users
def get_users(db: Session, skip:int=0, limit:int=100):
    return db.query(model.User).offset(skip).limit(limit).all()

#NOTE: we will use it tot get user by id
def get_user(db: Session, user_email: str ,user_id: int):
    user_exists = db.query(model.User).filter(model.User.email == user_email).first()
    # if user_exists #TODO: need to implement hash password
    return user_exists

# def get_allocated_email(db, user_email, user_id):
def get_allocated_email():
    try:
        return """
        A man tried to attack Kharat outside the court but the police stopped him in time and took him into custody.

Seeking further police remand for the accused godman who was arrested on March 18, public prosecutor Ajay Misar said new revelations about his illegal activities were surfacing every day.

It was even suspected that he could be involved in human sacrifice and hunting of deer for the skin and musk, among other things, the prosecution said.

The special investigation team probing the case has recovered a revolver, 21 cartridges and five empty shells besides ₹6 lakh in cash, two laptops and some documents from his possession, said the prosecution.

SIT officer, deputy Superintendent of Police Kirankumar Suryavanshi, also gave information about the probe to the court.
        """
    except Exception as e:
        print(f'Error in {func_name} . {get_allocated_email.__name__} : {e}')
        raise


def get_drafed_response():
    try:
        return " This is a sample draft response. Please review, edit ad needed and submit"
    except Exception as e:
        print(f'Error in {func_name} . {get_drafed_response.__name__} : {e}')
        raise

def get_user_hash_password(db:Session, email:str):
    try:
        print(f'Function is {get_user_hash_password.__name__}')
        user_password = db.query(model.User).filter(model.User.email == email).first()
        print(f'User_password : {user_password.password}') # NOTE: remove this print after testing
        return user_password.password
    except Exception as e:
        print(f'Error at {func_name} . {get_user_hash_password.__name__} : {e}')