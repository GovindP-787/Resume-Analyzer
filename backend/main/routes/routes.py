from fastapi import APIRouter, Depends, status, Query
from pydantic import BaseModel, Field
from typing import Optional
from fastapi import HTTPException
from sqlalchemy import text
from database import engine, get_db,SessionLocal
from models import Base, User, Resume
from sqlalchemy.orm import Session
from schemas import userCreate, user_response, user_update, user_patch_update, resume_response, resume_upload, ai
from sqlalchemy.exc import SQLAlchemyError
from fastapi import UploadFile, File
import os
from resume.pdf_reader import text_extracter
from ai.analyzer import analyze_resume

router = APIRouter()

@router.get("/")
def home():
    return {"message": "db connected"}

#create new user
@router.post("/users", response_model=user_response, status_code=status.HTTP_201_CREATED)
def create_user(user: userCreate, db: Session = Depends(get_db)):
    new_user = User(
        name=user.name,
        email=user.email
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database Error")

#show all users
@router.get("/users_all", response_model=list[user_response])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()

#show user by id
@router.get("/users/{user_id}", response_model=user_response)
def get_user(user_id: int, db:Session=Depends(get_db)):
    returned_user=db.query(User).filter(User.id == user_id).first()
    if returned_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return returned_user

#search user by name
@router.get("/users/name/search", response_model=user_response)
def get_user_by_name(user_name: str, db: Session = Depends(get_db)):
    returned_user = db.query(User).filter(User.name == user_name).first()
    if returned_user is None:
        return([])
    return returned_user

#pagination for users
@router.get("/users/all/pagination", response_model=list[user_response])
def paginated_users(skip: int = Query(default=0, ge=0), limit: int = Query(default=3, ge=1, le=100), db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

#show all resumes
@router.get("/resume/all", response_model=list[resume_response])
def get_all_resumes(db: Session = Depends(get_db)):
    resumes = db.query(Resume).all()
    if not resumes:
        raise HTTPException(status_code=404, detail="No resumes found")
    return resumes

#show resume by id
@router.get("/resume/{user_id}", response_model=list[resume_response])
def get_resume(user_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.user_id == user_id).all()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found for the user")
    return resume

#upload resume
# @router.post("/resume/upload", response_model=resume_response, status_code=status.HTTP_201_CREATED)
# def upload_resume(resume: resume_upload, db: Session = Depends(get_db)):
#     new_resume = Resume(
#         file_name=resume.file_name,
#         user_id=resume.user_id
#     )
#     try:
#         db.add(new_resume)
#         db.commit()
#         db.refresh(new_resume)
#         return new_resume
#     except SQLAlchemyError:
#         db.rollback()
#         raise HTTPException(status_code=500, detail="Database Error")
  
#upload resume   
@router.post("/resume/fileupload")
def upload_resume(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    file_content = text_extracter(file_path)
    if not file_content.strip():
        raise HTTPException(
            status_code=400,
            detail="No extractable text found in PDF"
        )

    new_resume = Resume(
        file_name=file.filename,
        user_id=user_id,
        text=file_content
    )

    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    return {
        "message": "Resume uploaded and processed successfully",
    "resume_id": new_resume.id,
    "file_name": new_resume.file_name,
    "user_id": new_resume.user_id,
    "extracted_text": file_content
    }

#delete resume
@router.delete("/resume/{resume_id}", response_model=list[resume_response])
def delete_resume(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).all()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    try:
        db.delete()
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database Error")
    return resume

#update user name and email
@router.put("/users/{user_id}", response_model=user_response)
def update_user(user_id: int, updated_user: user_update, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = updated_user.name
    db.commit()
    db.refresh(user)
    return user

#delete user
@router.delete("/users/{user_id}", response_model=user_response)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        db.delete(user)
        db.commit()
        return user
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database Error")

#update user name and email individually
@router.patch("/users/{user_id}", response_model=user_response)
def patch_user(user_id: int, updated_user: user_patch_update,db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if updated_user.name is not None:
        user.name = updated_user.name
    if updated_user.email is not None:
        user.email = updated_user.email
    db.commit()
    db.refresh(user)
    return user

#analyze resume
@router.post("/resume/{resume_id}/analyse")
def analyse_resume(resume_id: int, resquest: ai, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.user_id == resume_id).first()
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    if resume.text is None or resume.text.strip() == "":
        raise HTTPException(status_code=400, detail="No extractable text found in the resume")
    result = analyze_resume(resume.text, resquest.job_description)
    return {"analysis_result": result}