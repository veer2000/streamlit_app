import datetime

from fastapi import APIRouter, HTTPException, Depends
import httpx
from typing import Optional, Annotated
import pwdlib
from sqlalchemy.orm import Session

from ..services.utils import validate_password, get_session_id
from ..services.curd import get_user_hash_password, get_users, get_allocated_email_original, \
    get_user_by_id, change_password, add_data_to_email_status_detail, login_user_log_entry, find_user_log, \
    new_user_log_entry

# NOTE: we will keep model seperate
from ..services.model import User

from ..auth.deco import get_db, hash_arg

login_router = APIRouter(tags=["login API's"])


@login_router.get("/login")
def loginUser(email: str, password: str, passed_session_id, db: Session = Depends(get_db)):
    try:
        print('inside loginUser and before validate password')
        #NOTE: compare received password to password stored in DB in Userdb
        hashed_pass = get_user_hash_password(db, email)

        if not validate_password(password.encode('utf-8'), hashed_pass.encode('utf-8')):
            raise HTTPException(status_code=404, detail="Incorrect email or password")

        print('inside loginUser and after validate password')
        user_is = get_allocated_email_original(db, email, hashed_pass)
        user_log = find_user_log(db, email)

        if user_log:
            print(f'[DEBUG] Existing user_log found')

            if user_log.is_logged_in:
                print(f'[DEBUG] User already logged in')

                if user_log.session_id != passed_session_id:
                    print(f'[CONFLICT] session mismatch')
                    return {
                        "status": False,
                        "conflict": True,
                        "message": "Active session exists in another tab"
                    }
                else:
                    print(f'[DEBUG] Different browser → updating session')
                    # user_log.session_id = passed_session_id
                    user_log.is_logged_in = True
                    user_log.log_in_time = datetime.datetime.now()
                    user_log.log_out_time = None

                    db.commit()
                    return {
                        "user_id": user_is.id,
                        "user_name": user_is.name,
                        "status": True
                    }
            else:
                #NOTE:uses is already loggedin then we validate if diffrent session if diffrent session
                    #then close old session means old tab needs to be closed and new tab needs to be maintained
                    #need to find a way to automatically close old tab to maintain a flad for old tab and on shifting to
                    #that tab need to login or when opends old tab it autoatically checks if that tab is flagged as not to use
                    print(f' from else part of is loggedin ')
                    return user_is
                # print('[DEBUG] First time login')
                #
                # new_user_log_entry(
                #     user_email=email,
                #     is_logged_in=True,
                #     session_id=passed_session_id,
                #     db=db
                # )
        else:
            new_user_log_entry(
                user_email=email,
                is_logged_in=True,
                session_id=passed_session_id,
                db=db
            )

        user_is = get_allocated_email_original(db, email, hashed_pass)

        return {
            "user_id": user_is.id,
            "user_name":user_is.name,
            "status": True
        }
    #TODO: need to do late
    #FIXME: look
    except Exception as e:
        print(f'Error at {loginUser.__name__} error: {e}')
        raise HTTPException(status_code=401, detail="Login Failed")
# @login_router.get("/login")
# def loginUser(email:str, password: str, db:Session=Depends(get_db)): # request : Annotated[dict, Depends(get_db)]
#     try:
#         print(f' at loginUser method')
#         hashed_pass  = get_user_hash_password(db, email)
#         #NOTE: to validate_password params should be plantext as type = bytes and hashed as type = bytes for comparison
#         if validate_password(password.encode('utf-8'), hashed_pass.encode('utf-8')):
#             user_is = get_allocated_email_original(db, email, hashed_pass)
#             print(f'email is email {email} and users_data is {user_is.__dict__.copy()}')
#             login_user_log_entry(email, db)
#             return {"user_id":user_is.id,
#                     "status": True}
#         else:
#             raise HTTPException(status_code=404, detail="Incorrect email or password")
#         #TODO : find user by email : done
#         #TODO: using email get user details and validte : done
#     except Exception as e:
#         print(f'Error at {loginUser.__name__} error: {e}')
#         raise HTTPException(status_code=401, detail="Login Failed")


@login_router.post("/finduserbbyid")
async def findUserById(user_id: int, db: Session = Depends(get_db)):
    try:
        return get_user_by_id(db, user_id)
    except Exception as e:
        print(f'Error at {findUserById.__name__} error: {e}')
        raise


@login_router.get("/getallusers")
async def getaallusers(db:Session=Depends(get_db)):
    try:
        return get_users(db)
    except Exception as e:
        print(f'Error at {getaallusers.__name__} error: {e}')
        raise
@login_router.post("/adduser")
@hash_arg("password")
async def addUser(name: str, email: str, password: str, role :str ,db: Annotated[Session, Depends(get_db)],  password_original: Optional[str] = None,):
    try:
        new_user = User(
            email=email,
            name=name,
            role = role,
            password_original=password_original, #Note: store plain password
            password=password #Note: Storing hash password , NOT the plain text
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"user_id":new_user.id, "password":new_user.password}
    except Exception as e:
        print(f'Error at {addUser.__name__} error: {e}')
        raise

@login_router.post("/changepassword")
async def changePassword(email: str, password: str, db: Session = Depends(get_db)):
    try:
        return change_password(db, email, password)
    except Exception as e:
        print(f'Error at {changePassword.__name__} error: {e}')
        raise

# @login_router.post('/addeamilstatusdata')
# def insertRowToEmailStatusDetails(db: Session = Depends(get_db)):
#     return add_data_to_email_status_detail(tracking_data,db)