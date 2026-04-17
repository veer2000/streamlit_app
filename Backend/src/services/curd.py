import datetime

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
        # print(f'Email: {email}')
        # print(f'Function is {get_user_hash_password.__name__}')
        user_password = db.query(model.User).filter(model.User.email == email).first()
        if not user_password:
            print(f'User with email {email} does not exist')
        # print(f'User_password : {user_password.password}') # NOTE: remove this print after testing
        return user_password.password
    except Exception as e:
        print(f'Error at {func_name} . {get_user_hash_password.__name__} : {e}')

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

        # hashed_new_password = generate_hash_pass(new_password)
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
# Fetch from DB
def retrieve_drop_down_menu(db ):
    try:
        record = db.query(model.PriorityDetailList).filter(model.PriorityDetailList.id == 1).first()
        # print(f'type of result is {type(record)} result of get drop down {record} ')
        return record.options
    except Exception as e:
        print(f'Error at {retrieve_drop_down_menu.__name__} : {e}')
        raise

def retrieve_drop_down_menu_for_user(db):
    try:
        record = db.query(model.UserPriorityDetail.priority_name).all()
        result = tuple_of_list_to_list(record)
        return result
    except Exception as e:
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
        db.commit()
        print(f"Successfully updated priorities for User ID: {selected_id}")
        return True
    except Exception as e:
        print(f'Error in {add_priority_data_to_user.__name__} : {e}')
        raise


def add_data_to_email_status_detail(tracking_data, db):
    try:
        print(tracking_data)
        if tracking_data:
            for current_user in range(len(tracking_data)):
                print(f'current_user {current_user} and username :{tracking_data[current_user]["user"]}')
                existing_record = db.query(model.EmailStatusDetails).filter(
                    model.EmailStatusDetails.msg_id == tracking_data[current_user]["msg_id"],
                    model.EmailStatusDetails.user == tracking_data[current_user]["user"]
                ).first()
                print(f'database : {model.EmailStatusDetails.user} and to insert : {tracking_data[current_user]["user"]}')
                if existing_record:
                    print("Updating existing record")
                    existing_record.status = tracking_data[current_user]["status"]
                    existing_record.start_time = tracking_data[current_user]["start_time"]
                    existing_record.end_time = tracking_data[current_user]["end_time"]
                else:
                    print("Inserting new record")
                    new_record = model.EmailStatusDetails(
                        msg_id=tracking_data[current_user]["msg_id"],
                        user=tracking_data[current_user]["user"],
                        sender_email=tracking_data[current_user]["sender_email"],
                        subject=tracking_data[current_user]["subject"],
                        email_timestamp=tracking_data[current_user]["email_timestamp"],
                        status=tracking_data[current_user]["status"],
                        start_time=tracking_data[current_user]["start_time"],
                        end_time=tracking_data[current_user]["end_time"],
                    )
                    db.add(new_record)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f'Error in {add_data_to_email_status_detail.__name__} : {e}')
        raise



# ////////////////////////////////////////////////////////////////////////////////////////
def login_user_log_entry(user_email, db:Session):
    try:
        print('entered login_user_log_entry')
        loginlog = db.query(model.UserActivityLog).filter(model.UserActivityLog.user == user_email).first()
        if loginlog:
            print('entered if for login_user_log_entry')
            loginlog.log_in_time = datetime.datetime.now()
        else:
            new_log = model.UserActivityLog(
                user=user_email,
                log_in_time=datetime.datetime.now(),
                type = "user"
            )
            db.add(new_log)
            db.commit()
            db.refresh(new_log)

    except Exception as e:
        print(f'Error in {login_user_log_entry.__name__} : {e}')
        raise


def logout_user_log_entry(db:Session, user_email, type_is):
    try:
        logoutuser =  db.query(model.UserActivityLog).filter(model.UserActivityLog.user == user_email).first()
        if logoutuser:
            logoutuser.log_out_time = datetime.datetime.now()
            logoutuser.is_logged_in = False
            logoutuser.type = type_is
        db.commit()
        print(f'Successfully added logout time to Database')
        return True
    except Exception as e:
        print(f'Error in {logout_user_log_entry.__name__} : {e}')
        raise


def new_user_log_entry(user_email, is_logged_in, session_id,  db:Session):
    try:
        print('inside new_user_log_entry to add new entry')
        new_log = model.UserActivityLog(
            user=user_email,
            log_in_time=datetime.datetime.now(),
            is_logged_in= is_logged_in,
            session_id = session_id,
            type="user",
        )
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
    except Exception as e:
        print(f'Error in {new_user_log_entry.__name__} : {e}')
        raise


def find_user_log(db, email):
    try:
        return db.query(model.UserActivityLog).filter(model.UserActivityLog.user == email).first()
    except Exception as e:
        print(f'Error in {find_user_log.__name__} : {e}')
        raise