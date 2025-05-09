from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    key: int
    account: str
    status: int = 1
    teamkey: int = 0
    rolekey: int = 0
    
    class Config:
        orm_mode = True

class RoleSchema(BaseModel):
    key: int
    name: str
    status: int = 1
    
    class Config:
        orm_mode = True

class TeamSchema(BaseModel):
    key: int
    name: str
    status: int = 1
    
    class Config:
        orm_mode = True
