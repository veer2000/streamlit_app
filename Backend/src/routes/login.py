from fastapi import APIRouter, HTTPException, Depends
import httpx
from typing import Optional, Annotated
import pwdlib
from sqlalchemy.orm import Session

from ..services.utils import  validate_password
from ..services.curd import get_user_hash_password, get_users, get_allocated_email_original, \
    get_user_by_id, change_password, add_user_tracking_data

# NOTE: we will keep model seperate
from ..services.model import User

from ..auth.deco import get_db, hash_arg

login_router = APIRouter(tags=["login API's"])

@login_router.get("/login")
def loginUser(email:str, password: str, db:Session=Depends(get_db)): # request : Annotated[dict, Depends(get_db)]
    try:
        print(f' at loginUser method')
        hashed_pass  = get_user_hash_password(db, email)
        #NOTE: to validate_password params should be plantext as type = bytes and hashed as type = bytes for comparison
        if validate_password(password.encode('utf-8'), hashed_pass.encode('utf-8')):
            user_is = get_allocated_email_original(db, email, hashed_pass)
            return {"user_id":user_is.id,
                    "status": True}
        else:
            raise HTTPException(status_code=404, detail="Incorrect email or password")
        #TODO : find user by email : done
        #TODO: using email get user details and validte : done
    except Exception as e:
        print(f'Error at {loginUser.__name__} error: {e}')
        raise HTTPException(status_code=401, detail="Login Failed")


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

tracking_data = [
    {
        "msg_id":"AAMkAGRhN2M4ZjIyLTQ0ZmQtNGNiMi1hZDM4LTJmZGY3NjkwNmY3ZgBGAAAAAABadgoXVbP3R4yyxv4r5CRqBwAjLzc_n7YHS4d9ZMHcizm9AAEhyCo3AAAjLzc_n7YHS4d9ZMHcizm9AAEmu8suAAA=",
        "email_timestamp":"2026-03-24 06:04:46+00:00",
        "status":"Failed",
        "start_time":"2026-04-07 16h 58m 41s",
        "end_time":"2026-04-07 16h 58m 41s",
        "sender_email": "user1@mail.com",
        "subject": "test",
        "user":"don"
    },
    {
        "msg_id":"AAMkAGRhN2M4ZjIyLTQ0ZmQtNGNiMi1hZDM4LTJmZGY3NjkwNmY3ZgBGAAAAAABadgoXVbP3R4yyxv4r5CRqBwAjLzc_n7YHS4d9ZMHcizm9AAEhyCo3AAAjLzc_n7YHS4d9ZMHcizm9AAEmu8stAAA=",
        "email_timestamp":"2026-03-24 06:35:18+00:00",
        "status":"Not Started",
        "start_time":"2026-04-07 16h 58m 41s",
        "end_time":"2026-04-07 16h 58m 41s",
        "sender_email": "user1@mail.com",
        "subject": "test",
        "user":"mouse"
    },
    {
        "msg_id":"AAMkAGRhN2M4ZjIyLTQ0ZmQtNGNiMi1hZDM4LTJmZGY3NjkwNmY3ZgBGAAAAAABadgoXVbP3R4yyxv4r5CRqBwAjLzc_n7YHS4d9ZMHcizm9AAEhyCo3AAAjLzc_n7YHS4d9ZMHcizm9AAEmu8ssAAA=",
        "email_timestamp":"2026-03-24 06:43:45+00:00",
        "status":"Completed",
        "start_time":"2026-04-07 16h 58m 41s",
        "end_time":"2026-04-07 16h 58m 41s",
        "sender_email": "user1@mail.com",
        "subject": "test",
        "user":"pen"
    },
    {
        "msg_id":"AAMkAGRhN2M4ZjIyLTQ0ZmQtNGNiMi1hZDM4LTJmZGY3NjkwNmY3ZgBGAAAAAABadgoXVbP3R4yyxv4r5CRqBwAjLzc_n7YHS4d9ZMHcizm9AAEhyCo3AAAjLzc_n7YHS4d9ZMHcizm9AAEmu8srAAA=",
        "email_timestamp":"2026-03-24 06:50:22+00:00",
        "status":"Not Started",
        "start_time":"2026-04-07 16h 58m 41s",
        "end_time":"2026-04-07 16h 58m 41s",
        "sender_email": "user1@mail.com",
        "subject": "test",
        "user":"wire"
    }
]

@login_router.post('/addusertrackingdata')
def addusertrackingdata(db: Session = Depends(get_db)):
    return add_user_tracking_data(tracking_data,db)