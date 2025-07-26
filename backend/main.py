from fastapi import FastAPI
from app.database import get_engine, Base
from app.models import item, user, post, post
from app.routers import auth, posts

app = FastAPI()

@app.on_event("startup")
def on_startup():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(posts.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
