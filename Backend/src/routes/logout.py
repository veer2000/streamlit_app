from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from ..auth.deco import get_db
from ..services.curd import logout_user_log_entry

logout_api = APIRouter(tags=["logout API"])


@logout_api.get("/logout")
def logout(db:Session = Depends(get_db)):
    return logout_user_log_entry(db, user_email="")
