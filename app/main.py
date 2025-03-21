from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings


# models.Base.metadata.create_all(bind=engine) create all tables. alembic handles this now, no longer needed

origins = ['https://www.google.com']

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello world!"}
