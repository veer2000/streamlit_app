from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..auth.deco import get_db
from ..services.curd import add_data_to_email_status_detail

email_router = APIRouter(tags=['Email Status API'])


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
    },
    {
        "msg_id": "AAMkAGRhN2M4ZjIyLTQ0ZmQtNGNiMi1hZDM4LTJmZGY3NjkwNmY3ZgBGAAAAAABadgoXVbP3R4yyxv4r5CRqBwAjLzc_n7YHS4d9ZMHcizm9AAEhyCo3AAAjLzc_n7YHS4d9ZMHcizm9AAEmu8stAAA=",
        "email_timestamp": "2026-03-24 06:50:22+00:00",
        "status": "Not Started",
        "start_time": "2026-04-07 16h 58m 41s",
        "end_time": "2026-04-07 16h 58m 41s",
        "sender_email": "user1@mail.com",
        "subject": "test",
        "user": "charger"
    },
    {
        "msg_id": "AAMkAGRhN2M4ZjIyLTQ0ZmQtNGNiMi1PZDM4LTJmZGY3NjkwNmY3ZgBGAAAAAABadgoXVbP3R4yyxv4r5CRqBwAjLzc_n7YHS4d9ZMHcizm9AAEhyCo3AAAjLzc_n7YHS4d9ZMHcizm9AAEmu8arAAA=",
        "email_timestamp": "2026-03-24 06:50:22+00:00",
        "status": "Not Started",
        "start_time": "2026-04-07 16h 58m 41s",
        "end_time": "2026-04-07 16h 58m 41s",
        "sender_email": "user1@mail.com",
        "subject": "test",
        "user": "bottle"
    },
    {
        "msg_id": "AAMkAGRhN2M4ZjIyLTQ0ZmQtNGNiMi1hSDM4LTJmZGY3NjkwNmY3ZgBGAAAAAABadgoXVbP3R4yyxv4r5CRqBwAjLzc_n7YHS4d9ZMHcizm9AAEhyCo3AAAjLzc_n7YHS4d9ZMHcizm9AAEmu8prAAA=",
        "email_timestamp": "2026-03-24 06:50:22+00:00",
        "status": "Not Started",
        "start_time": "2026-04-07 16h 58m 41s",
        "end_time": "2026-04-07 16h 58m 41s",
        "sender_email": "user1@mail.com",
        "subject": "test",
        "user": "book"
    },    {
        "msg_id":"AAMkAGRhN2M4ZjIyLTQ0ZmQtNGNiMi2hZDM4LTJmZGY3NjkwNmY3ZgBGAAAAAABadgoXVbP3R4yyxv4r5CRqBwAjLzc_n7YHS4d9ZMHcizm9AAEhyCo3AAAjLzc_n7YHS4d9ZMHcizm9AAEmu9vrAAA=",
        "email_timestamp":"2026-03-24 06:50:22+00:00",
        "status":"Completed",
        "start_time":"2026-04-07 16h 58m 41s",
        "end_time":"2026-04-07 16h 58m 41s",
        "sender_email": "user1@mail.com",
        "subject": "test",
        "user":"eraser"
    },
]


@email_router.post('/addeamilstatusdata')
def insertRowToEmailStatusDetails(db: Session = Depends(get_db)):
    return add_data_to_email_status_detail(tracking_data,db)