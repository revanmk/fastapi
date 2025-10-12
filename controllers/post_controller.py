
from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from models import Post  # SQLAlchemy model
from schemas import PostBase  # Pydantic schema
from database import engine, Base

router = APIRouter(prefix="/posts", tags=["posts"])
Base.metadata.create_all(bind=engine)

@router.post("/post/")
async def create_post(post: PostBase, db: Session = Depends(get_db)):
    new_post = Post(
        title=post.title,
        content=post.content,
        published=post.published
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # get ID and updated fields
    return new_post

@router.get("/posts/")
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts

@router.get("/post/{id}")
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    return post

@router.put("/post/{id}")
async def update_post(id: int, updated_post: PostBase, db: Session = Depends(get_db)):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()
    if post:
        post_query.update(updated_post.dict(), synchronize_session=False)
        db.commit()
        return post_query.first()
    return {"error": "Post not found"}
@router.delete("/post/{id}")
async def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()
    if post:
        post_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Post deleted"}
    return {"error": "Post not found"}
    