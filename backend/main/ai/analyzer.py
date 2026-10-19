import os

from dotenv import load_dotenv
from google import genai
from ai.retrieval import retrieve_chunks

load_dotenv()

client = genai.Client(api_key=os.getenv("RESUME_KEY"))

def analyze_resume(resume_text: str, job_description: str):
    results = retrieve_chunks(query = job_description, document = resume_text, chunk_size = 500, overlap = 100, top_k = 3)
    for i, result in enumerate(results, start=1):
        print(f"\n--- Retrieved Chunk {i} ---")
        print(f"Similarity: {result['score']:.4f}")
        print(result["chunk"])

    relevant_resume = "\n\n".join(
        result["chunk"] for result in results
    )

    prompt = f"""
    You are an evidence-based technical recruiter.

    Analyze the resume against the job description.

    RESUME:
    {resume_text}

    JOB DESCRIPTION:
    {job_description}

    Instructions:
    1. Evaluate each required skill separately.
    2. Use only evidence explicitly present in the resume.
    3. Never assume a candidate knows a technology because they
    have used a related framework, library, or tool.
    4. Distinguish between:
    - Demonstrated skills
    - Missing or unverified skills
    - Transferable experience
    5. Do not invent qualifications, dates, or experience.
    6. If a date appears to be in the future, flag it for verification
    instead of assuming it is a typo.
    7. Explain the evidence behind every assessment.
    8. Give a match score out of 100 based on the actual requirements,
    and explain the scoring rationale.

    Return:
    1. Required Skills Assessment
    2. Relevant Skills Found
    3. Missing or Unverified Skills
    4. Relevant Experience
    5. Resume Strengths
    6. Areas for Improvement
    7. Match Score and Scoring Rationale
    8. Recruiter Summary
    """
    response = client.models.generate_content(
   model="gemini-3.5-flash",
   contents=prompt
    )
    
    return response.text    