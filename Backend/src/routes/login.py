from fastapi import APIRouter, HTTPException, Depends
import httpx
from typing import Optional, Annotated
import pwdlib
from sqlalchemy.orm import Session

from ..auth.deco import hash_pass, validate_password
from ..services.curd import get_allocated_email, get_user_hash_password

# NOTE: we will keep model seperate
from ..services.model import User

from ..auth.deco import get_db


login_router = APIRouter(tags=["login API's"])

@login_router.get("/login")
async def loginUser(email:str, password: str,db:Session=Depends(get_db)): # request : Annotated[dict, Depends(get_db)]
    try:
        # hash_generate = hash_pass(password)
        # print(hash_generate)
        hashed_pass  = get_user_hash_password(db, email)
        #NOTE: to validate_password params should be plantext as type = bytes and hashed as type = bytes for comparison
        if validate_password(password.encode('utf-8'), hashed_pass.encode('utf-8')):
            user_is =get_allocated_email(db, email, password)
            print(f'User_id is {user_is.id}')
            return user_is.id
        else:
            raise HTTPException(status_code=404, detail="Incorrect email or password")

        #TODO : find user by email : done

        #TODO: using email get user details and validte : done
        # print(request)
    except Exception as e:
        print(f'Error at {loginUser.__name__} error: {e}')
        raise HTTPException(status_code=401, detail="Login Failed")


@login_router.post("/adduser")
async def addUser(name: str, email: str, password: str, db: Annotated[Session, Depends(get_db)]):
    try:
        hash_generate = hash_pass(password)
        print(hash_generate)
        new_user = User(
            email=email,
            name=name,
            password=hash_generate # Store the hash, NOT the plain text
        )
        # 3. Save to database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"user_id":new_user.id, "password":new_user.password}
    except Exception as e:
        print(f'Error at {addUser.__name__} error: {e}')
        raise
