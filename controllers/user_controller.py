from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User  # SQLAlchemy model
from schemas import UserOut,UserBase  # Pydantic schema
from database import engine, Base
from fastapi import APIRouter, HTTPException, status
from passlib.context import CryptContext
from typing import List

router = APIRouter(prefix="/users", tags=["users"])
Base.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/user/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: Session = Depends(get_db)):
    db_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password
    new_user = User(
        username=user.username,
        email = user.email,
        password=user.password,
        full_name=user.full_name,
        disabled=user.disabled
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # get ID and updated fields
    return new_user

@router.get("/{user_id}",response_model=UserOut)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
@router.get("/", response_model=List[UserOut])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return
@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, updated_user: UserBase, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if updated_user.password:
        updated_user.password = pwd_context.hash(updated_user.password)
    for key, value in updated_user.dict(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user
