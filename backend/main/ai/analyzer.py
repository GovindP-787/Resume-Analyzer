import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("RESUME_KEY"))

def analyze_resume(resume_text: str, job_description: str):
    prompt = f"""
    You are an expert technical recruiter.

    Analyze the following resume against the job description.

    RESUME:
    {resume_text}

    JOB DESCRIPTION:
    {job_description}

    Provide:
    1. Relevant skills found in the resume.
    2. Important missing skills.
    3. Resume strengths.
    4. Areas for improvement.
    5. An overall match score out of 100.

    Return the response in a clear, structured format.
    """
    response = client.models.generate_content(
   model="gemini-3.5-flash",
   contents=prompt
    )

    return response.text    