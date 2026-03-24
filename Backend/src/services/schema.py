from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserInDB(UserBase):
    id: int
    password: str  # lets use hashed #TODO: we need a logic to hash the password and store it to return and compare
    createddate: datetime

    model_config = ConfigDict(from_attributes=True)



class UserPublic(UserBase):
    id: int
    createddate: datetime

    model_config = ConfigDict(from_attributes=True)
