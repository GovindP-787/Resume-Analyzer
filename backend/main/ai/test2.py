from analyzer import analyze_resume
resume = """
Python developer.
Skills: Python, FastAPI, PostgreSQL, React.
Projects: Built a REST API using FastAPI.
"""

job_description = """
Looking for a junior backend developer.
Required skills: Python, FastAPI, PostgreSQL, Docker.
"""

result = analyze_resume(resume, job_description)

print(result)