from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship

from ..services.database import Base

class User(Base):
    __tablename__ = "users"
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
    id = Column(Integer,primary_key=True,index=True)
    options =Column(JSON)