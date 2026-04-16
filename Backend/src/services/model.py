from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship

from ..services.database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(255),index=True)
    email = Column(String(255), unique=True, index=True)
    priority1 =Column(String(255),index=True)
    priority2 =Column(String(255),index=True)
    priority3 =Column(String(255),index=True)
    role = Column(String(255),index=True)
    password_original =Column(String(255))
    password = Column(String(255))
    createdate = Column(DateTime,default=datetime.now)

    def to_dict(self):
        """Convert SQLAlchemy object to a clean dictionary."""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }


class PriorityDetailList(Base):
    __tablename__ = "priority_detail_list"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer,primary_key=True,index=True)
    options =Column(JSON)

class UserPriorityDetail(Base):
    __tablename__ = "user_priority_detail"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer,primary_key=True,index=True)
    priority_name = Column(String(255))
    priority_detail = Column(String(255))
    created_at =  Column(DateTime,default=datetime.now)

class EmailStatusDetails(Base):
    __tablename__ = "email_status_details"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer,primary_key=True,index=True)
    msg_id = Column(String(255))
    user = Column(String(255))
    sender_email = Column(String(255))
    subject = Column(String(255))
    email_timestamp = Column(String(255))
    status = Column(String(255))
    start_time = Column(String(255))
    end_time = Column(String(255))
    created_time =  Column(DateTime,default=datetime.now)



class UserActivityLog(Base):
    __tablename__ = "user_log_activity"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer,primary_key=True,index=True)
    user = Column(String(255),index=True)
    log_in_time = Column(String(255),index=True)
    log_out_time = Column(String(255),index=True,nullable=True)
    is_logged_in = Column(Boolean, default=False)
    session_id = Column(String(255), nullable=True)
    type = Column(String(255))