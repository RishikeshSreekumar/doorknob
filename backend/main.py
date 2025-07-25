from fastapi import FastAPI
from fastapi import FastAPI
from .app.database import get_engine, Base
from .app.models import item, user
from .app.routers import auth

app = FastAPI()

@app.on_event("startup")
def on_startup():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)

app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
