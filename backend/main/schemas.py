
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class userCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr

class user_response(BaseModel):
    id: int
    name: str
    email: str
    model_config = ConfigDict(from_attributes=True)

class user_update(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr

class user_patch_update(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=50)
    email: EmailStr | None = None

class resume_response(BaseModel):
    id: int
    file_name: str
    user_id: int
    model_config = ConfigDict(from_attributes=True)

class resume_upload(BaseModel):
    file_name: str = Field(min_length=1, max_length=100)
    user_id: int

class ai(BaseModel):
    job_description: str
   