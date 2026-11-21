import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from schemas import ResumeAnalysis
from lang_retriever import retrieve_chunks

load_dotenv()


# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("RESUME_KEY"),
    temperature=0
)

# Configure structured output
structured_llm = llm.with_structured_output(ResumeAnalysis)


def analyze_resume(
    resume_id: int,
    job_description: str
) -> ResumeAnalysis:

    # 1. Retrieve relevant resume chunks
    results = retrieve_chunks(
        query=job_description,
        resume_id=resume_id,
        k=5
    )

    if not results:
        raise ValueError("No relevant resume evidence found in ChromaDB")

    # 2. Construct resume evidence
    relevant_resume = "\n\n".join(
        result.page_content for result in results
    )

    # 3. Create the prompt
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are an evidence-based technical recruiter.

            Evaluate the resume against the job description.

            RESUME EVIDENCE:
            {resume_evidence}

            JOB DESCRIPTION:
            {job_description}

            Rules:
            1. Evaluate each job requirement separately.
            2. Use only evidence present in the supplied resume evidence.
            3. Do not assume proficiency from a skill name alone.
            4. Distinguish demonstrated, partially demonstrated,
               missing, and unverified skills.
            5. Do not invent experience, qualifications, or dates.
            6. Treat missing evidence as missing from retrieved evidence,
               not proof that the candidate lacks the skill.
            7. Keep technical match scores separate from resume flags.
            8. Alternative skills connected by OR should be treated
               as alternatives.
            9. Distribute requirement weights consistently.
            10. Do not award points for unrelated supporting skills.

            Scoring:
            - Every requirement must have a score and max_score.
            - Scores must be between zero and their maximum.
            - Give each requirement an appropriate max_score.
            - Do not calculate the overall match_score yourself.
            - Python will calculate the final match score.

            Return:
            - requirements
            - relevant_skills
            - strengths
            - improvement_areas
            - resume_flags
            - recruiter_summary

            Use only these requirement statuses:
            demonstrated, partially_demonstrated, missing, unverified.

            Use only these resume flag types:
            date_verification, missing_information,
            inconsistency, other.

            Evidence must always be a list of strings.
            If no evidence is found, return an empty list.
            """
        )
    ])

    # 4. Combine prompt and model
    chain = prompt | structured_llm

    # 5. Generate structured analysis
    analysis = chain.invoke({
        "resume_evidence": relevant_resume,
        "job_description": job_description
    })

    # 6. Calculate final score using Python
    total_score = sum(
        requirement.score
        for requirement in analysis.requirements
    )

    total_max_score = sum(
        requirement.max_score
        for requirement in analysis.requirements
    )

    if total_max_score > 0:
        analysis.match_score = round(
            (total_score / total_max_score) * 100
        )

    return analysis