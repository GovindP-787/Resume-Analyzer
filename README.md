# Resume Analyzer

Resume Analyzer is a work-in-progress full-stack application for comparing a PDF resume with a job description. It extracts resume text, retrieves relevant passages, and produces a structured, evidence-based analysis.

## What is implemented

- A FastAPI backend with user and resume endpoints.
- PDF text extraction and resume storage using SQLAlchemy.
- Resume chunking and vector indexing with LangChain and ChromaDB.
- Job-description-based analysis using Google Gemini, including a match score, requirement assessments, evidence, strengths, improvement areas, and recruiter summary.
- Persistence of analysis results in the database.
- An early React and TypeScript interface for uploading a PDF, entering a job description, and viewing the analysis response.

## Technologies

- **Frontend:** React, TypeScript, Vite, Tailwind CSS
- **Backend:** Python, FastAPI, SQLAlchemy, Alembic
- **AI and retrieval:** LangChain, Google Gemini, ChromaDB
- **PDF processing:** PyMuPDF

## Project status

This project is under active development. The backend upload and analysis workflow is in place, while the frontend and overall product experience are still evolving.
