from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas
from ..models import post, user
from ..database import get_db
from ..auth import get_current_user

router = APIRouter()

@router.post("/posts/", response_model=schemas.Post)
def create_post(post_data: schemas.PostCreate, db: Session = Depends(get_db), current_user: user.User = Depends(get_current_user)):
    db_post = post.Post(**post_data.dict(), owner_id=current_user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/posts/{post_id}", response_model=schemas.Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(post.Post).filter(post.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@router.put("/posts/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, post_data: schemas.PostCreate, db: Session = Depends(get_db), current_user: user.User = Depends(get_current_user)):
    db_post = db.query(post.Post).filter(post.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
    for var, value in vars(post_data).items():
        setattr(db_post, var, value) if value else None
    db.commit()
    db.refresh(db_post)
    return db_post

@router.delete("/posts/{post_id}", response_model=schemas.Post)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: user.User = Depends(get_current_user)):
    db_post = db.query(post.Post).filter(post.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    db.delete(db_post)
    db.commit()
    return db_post
