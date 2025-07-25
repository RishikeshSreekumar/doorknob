from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os

app = FastAPI()

# CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for posts
posts = []
UPLOAD_DIR = "uploads"

# Create the upload directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)


class Post(BaseModel):
    text: str
    image_url: str


@app.post("/posts/", response_model=Post)
async def create_post(text: str = Form(...), image: UploadFile = File(...)):
    # Save the uploaded image
    image_path = os.path.join(UPLOAD_DIR, image.filename)
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # Create a new post
    post = Post(text=text, image_url=f"/{image_path}")
    posts.append(post)
    return post


@app.get("/posts/", response_model=list[Post])
async def get_posts():
    return posts
@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}
