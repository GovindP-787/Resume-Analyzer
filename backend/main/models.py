from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON, DateTime, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    resume = relationship("Resume", back_populates="user")

class Resume(Base):
    __tablename__ = "resume"
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="resume")
    text = Column(Text, nullable=True)  
    analyses = relationship("Analysis", back_populates="resume")

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer,ForeignKey("resume.id"),nullable=False)
    job_description = Column(Text, nullable=False)
    analysis_result = Column(JSON, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    resume = relationship("Resume", back_populates="analyses")