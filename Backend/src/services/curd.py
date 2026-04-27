from datetime import datetime

from sqlalchemy.orm import Session
import streamlit as st

from .helper import tuple_of_list_to_list
from .model import User
from ..auth.deco import hash_arg
from ..services import model, schema
import inspect
# from .utils import generate_hash_pass


func_name = inspect.currentframe().f_code.co_name

#NOTE: we will use it to get all users
def get_users(db: Session, skip:int=0, limit:int=100):
    all_users = db.query(model.User).offset(skip).limit(limit).all()
    return [user.to_dict() for user in all_users]

#NOTE: we will use it tot get user by id
def get_user_by_id(db: Session, user_id: int):
    user_exists = db.query(model.User).filter(model.User.id == user_id).first()
    # if user_exists #TODO: need to implement hash password
    return user_exists

#NOTE: this method is for DB logic logic
def get_allocated_email_original(db, user_email, user_password):
    try:
        user_identity =  db.query(model.User).filter(model.User.email == user_email).first()
        return user_identity
    except Exception as e:
        print(f'Error in {func_name} . {get_allocated_email_original.__name__} : {e}')
        raise

def get_allocated_email(db : Session, email : str, password):
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


def get_draft_response(emailContent):
    try:
        return emailContent
        # return " This is a sample draft response. Please review, edit ad needed and submit"
    except Exception as e:
        print(f'Error in {func_name} . {get_draft_response.__name__} : {e}')
        raise

def get_user_hash_password(db:Session, email:str):
    try:
        user_password = db.query(model.User).filter(model.User.email == email).first()
        if not user_password:
            print(f'User with email {email} does not exist')
        return user_password.password
    except Exception as e:
        print(f'Error at {func_name} . {get_user_hash_password.__name__} : {e}')
        raise

def submit_response(response):
    try:
        return response
    except Exception as e:
        print(f'Error in {func_name} . {submit_response.__name__} : {e}')
        raise

@hash_arg("new_password")
def change_password(db:Session, user_email:str, new_password:str):
    try:
        update_user_password = db.query(model.User).filter(model.User.email == user_email).first()
        if not update_user_password:
            return {"status": False, "message": "User does not exist"}

        change_password.password = new_password
        update_user_password.password = new_password
        db.commit()
        db.refresh(update_user_password)
        return {"status": True, "message": "Password changed successfully"}
    except Exception as e:
        print(f'Error in {func_name} . {change_password.__name__} : {e}')
        db.rollback()
        raise


#----------------------------------------------------------------------------------------------------------------------
def retrieve_drop_down_menu_for_user(db):
    try:
        record = db.query(model.UserPriorityDetail.priority_name).all()
        result = tuple_of_list_to_list(record)
        return result
    except Exception as e:
        print(f'Error in {func_name} . {retrieve_drop_down_menu_for_user.__name__} : {e}')
        raise

def retrieve_drop_down_menu_for_specific_user(db, user_name):
    try:
        reterived_priority = db.query(model.User.priority1, model.User.priority2, model.User.priority3 ).filter(model.User.name == user_name).first()
        if reterived_priority and all(val and val.strip() for val in reterived_priority):
            return reterived_priority

        return None
    except Exception as e:
        print(f'Error at retrieve_drop_down_menu_for_specific_user :{e}')
        raise

# @st.cache_data
def retrieve_drop_down_of_users(_db):
    try:
        # NOTE: if you want user id fetched for database it is already retrieved just need to change how to send retriever right now we only send name
        user_records = _db.query(User.id, User.name).filter(User.role != "admin").all()
        return {user.name: user.id for user in user_records}
    except Exception as e:
        print(f'Error in {retrieve_drop_down_of_users.__name__} : {e}')
        raise

def add_priority_data_to_user(db,selected_id, user, priority1, priority2, priority3):
    try:
        user_to_update = db.query(model.User).filter(model.User.id == selected_id).first()
        if user_to_update:
            user_to_update.priority1 = priority1
            user_to_update.priority2 = priority2
            user_to_update.priority3 = priority3
            user_to_update.createdate = datetime.now()
        db.commit()
        return True
    except Exception as e:
        print(f'Error in {add_priority_data_to_user.__name__} : {e}')
        raise