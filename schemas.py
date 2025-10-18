from pydantic import BaseModel, EmailStr
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass
class PostOut(PostBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    disabled: bool = False

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    disabled: bool = False

    class Config:
        orm_mode = True
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    id: Optional[str] = None
