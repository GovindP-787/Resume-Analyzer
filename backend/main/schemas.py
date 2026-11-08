
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator
from typing import Literal

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

class skill_assessment(BaseModel):
    skill: str
    status: Literal["demonstrated","partially_demonstrated", "missing", "unverified"]
    evidence: list[str] = Field(default_factory=list)
    score: float = Field(ge=0)
    max_score: float = Field(gt=0)
    @model_validator(mode="after")
    def validate_score(self):
        if self.score > self.max_score:
            raise ValueError("Score cannot be greater than max_score")
        return self

class resume_flag(BaseModel):
    type: Literal[
        "date_verification",
        "missing_information",
        "inconsistency",
        "other"
    ]
    message: str

class ResumeAnalysis(BaseModel):
    match_score: float = Field(ge=0, le=100)
    requirements: list[skill_assessment]
    relevant_skills: list[str]
    strengths: list[str]
    improvement_areas: list[str]
    resume_flags: list[resume_flag]
    recruiter_summary: str

