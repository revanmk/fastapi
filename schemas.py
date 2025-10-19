from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic.types import conint

# ---------- POST SCHEMAS ----------
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):  # 👈 Define UserOut BEFORE using it
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    disabled: bool = False

    class Config:
        orm_mode = True
        
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)  # 1 for upvote, 0 for remove vote

class PostOut(PostBase):
    id: int
    user: UserOut  # 👈 No quotes needed now
    class Config:
        orm_mode = True

class PostWithVotes(BaseModel):
    Post: PostOut
    votes: int

    class Config:
        orm_mode = True

# ---------- USER SCHEMAS ----------
class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    disabled: bool = False


# ---------- TOKEN SCHEMAS ----------
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
