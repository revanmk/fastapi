from typing import List
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Post
from schemas import PostBase, PostCreate, PostOut
import oauth2

router = APIRouter(prefix="/posts", tags=["Posts"])


# Create a Post
@router.post("/", response_model=PostOut, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    new_post = Post(**post.dict(), user_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# Get All Posts
@router.get("/", response_model=List[PostOut])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts


# Get Single Post
@router.get("/{id}", response_model=PostOut)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    return post


# Update Post
@router.put("/{id}", response_model=PostOut)
async def update_post(
    id: int,
    updated_post: PostBase,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to update this post")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


# Delete Post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to delete this post")

    post_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "Post deleted successfully"}
