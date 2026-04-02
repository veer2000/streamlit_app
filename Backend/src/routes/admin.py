from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..auth.deco import get_db
from ..services.curd import retrieve_drop_down_menu, retrieve_drop_down_of_users

admin_routes = APIRouter(tags=["Admin API's"])


@admin_routes.get("/retrieve_drop_down_menu")
def all_drop_down_values(db:Session=Depends(get_db)):
    try:
        return retrieve_drop_down_menu(db)
    except Exception as e:
        print(f'Error at {all_drop_down_values.__name__} : {e}')
        raise

@admin_routes.get("/retrieve_drop_for_users")
def retrieve_drop_down_for_users(db:Session=Depends(get_db)):
    try:
        return retrieve_drop_down_of_users(db)
    except Exception as e:
        print(f'Error at {retrieve_drop_down_for_users.__name__} : {e}')
        raise
