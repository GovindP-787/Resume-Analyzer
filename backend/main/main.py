from fastapi import FastAPI, Depends, status, Query
from pydantic import BaseModel, Field
from typing import Optional
from fastapi import HTTPException
from database import engine, get_db,SessionLocal
from models import Base, User
from sqlalchemy.orm import Session
from schemas import userCreate, user_response, user_update, user_patch_update
from sqlalchemy.exc import SQLAlchemyError
from routes.routes import router
from ai.analyzer import retrieve_chunks


app = FastAPI()
app.include_router(router)

# class User(BaseModel):
#     name: str
#     age: Optional[int] = None
#     experience: int = Field(default=0, ge=0, le=15)

@app.get("/")
def home():
    return {"message": "db connected"}

# @app.get("/skills/{skill_name}/{limit}")
# def skills(skill_name: str, limit: int = 10):
#     return({"skill name": skill_name, "limit": limit})

# @app.get("/users/{user_id}")
# def user(user_id: int):
#     return{"user ID": user_id}

# @app.post("/users")
# def create_user(user: User):
#     return{
#         "name:": user.name,
#         "age:": user.age,
#         "experience": user.experience
#     }

# @app.post("/users/{user_id}")
# def update_user(user_id: int):
#     if (user_id <= 0 or user_id > 100):
#         raise HTTPException(status_code=400, detail="User ID must be a positive integer")
#     return {"user ID": user_id}

Base.metadata.create_all(bind=engine)
