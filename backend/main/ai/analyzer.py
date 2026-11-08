import json
import os

from dotenv import load_dotenv
from google import genai
from ai.retrieval import retrieve_chunks
from schemas import ResumeAnalysis, skill_assessment

load_dotenv()

client = genai.Client(api_key=os.getenv("RESUME_KEY"))

def analyze_resume(resume_text: str, job_description: str) -> ResumeAnalysis:
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

    Evaluate the resume against the job description.

    RESUME EVIDENCE:
    {relevant_resume}

    JOB DESCRIPTION:
    {job_description}

    Rules:
    1. Evaluate each job requirement separately.
    2. Use only evidence present in the supplied resume evidence.
    3. Do not assume proficiency from a skill name alone.
    4. Distinguish demonstrated, partially demonstrated,
    not found, and unverified skills.
    5. Do not invent experience, qualifications, or dates.
    6. Treat missing evidence as "not found in retrieved evidence",
    not proof that the candidate lacks the skill.
    7. Keep technical match scores separate from resume flags.
    8. Do not guess corrections for questionable dates.
    9. Return valid JSON matching the requested schema.

    Scoring:
    - Each requirement must have a score and max_score.
    - A score must be between zero and its maximum.
    - Alternative skills connected by OR should be treated as alternatives.
    - Calculate the overall match_score from the requirement scores.
    - Distribute requirement weights consistently so they total 100.
    - Do not award points for unrelated supporting skills.

    Return a JSON object with these fields:
    - match_score: number from 0 to 100
    - requirements: array of objects containing skill, status,
    evidence, score, max_score
    - relevant_skills: array of strings
    - strengths: array of strings
    - improvement_areas: array of strings
    - resume_flags: array of objects containing type and message
    - recruiter_summary: string

    Allowed requirement statuses:
    - demonstrated
    - partially_demonstrated
    - missing
    - unverified

    Output rules:
    - Each requirement must use the key "skill", not "skills".
    - Each requirement's "evidence" must be a list of strings.
    - If no evidence is found, return an empty list for "evidence".
    - Never return a single string where a list is required.
    - Use only the four allowed status values.

    Allowed resume flag types:
    date_verification, missing_information, inconsistency, other

    Return only the JSON object. Do not use Markdown code fences.
    """

    try:
        response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt

        )

        try:
            result_data = json.loads(response.text)
            analysis = ResumeAnalysis.model_validate(result_data)
            total_score = sum(requirement.score for requirement in analysis.requirements)
            total_max_score = sum(requirement.max_score for requirement in analysis.requirements)
            if total_max_score > 0:
                analysis.match_score = round((total_score / total_max_score) * 100
    )

            print("Expected fields:", skill_assessment.model_fields.keys())
            print("Gemini fields:", result_data["requirements"][0].keys())
            
            return analysis

        except json.JSONDecodeError as e:
            print("Gemini returned invalid JSON:")
            print(response.text)
            raise ValueError("AI returned invalid JSON") from e

        except Exception as e:
            print("AI response validation failed:")
            print(e)
            print(response.text)
            raise
    except Exception as e:
        print("Gemini API error")
        print("Status code:", e.code)
        print("Message:", e.message)
        raise