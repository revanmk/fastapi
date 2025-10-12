from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
import oauth2
from models import User
from utils import verify_password

router = APIRouter(prefix="/oauth2", tags=["oauth2"])
from schemas import Token,TokenData
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

@router.post("login", response_model=TokenData)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    access_token = oauth2.create_access_token(data={"user_id": user.id, "username": user.username})
    return {"access_token": access_token, "token_type": "bearer"}