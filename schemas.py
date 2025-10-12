from pydantic import BaseModel, EmailStr
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

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

from pydantic import BaseModel
from typing import Optional

# Existing models like UserBase, PostBase...

class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None
    exp: Optional[int] = None