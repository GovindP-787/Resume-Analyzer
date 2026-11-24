
from lang_splitter import split_resume
from lang_embeddings import get_embeddings
from lang_document import create_langchain_document
from lang_vectorstore import vector_store_db
from lang_retriever import retrieve_chunks
from lang_analyzer import analyze_resume


# 1. Sample resume text
resume_text = """
Python developer with experience in FastAPI and PostgreSQL.
Developed React applications and worked with REST APIs.
"""


# 2. Create LangChain document
doc = create_langchain_document(
    resume_text=resume_text,
    resume_id=101,
    file_name="test.pdf"
)


# 3. Split resume into chunks
chunks = split_resume(doc)

print("\n--- GENERATED CHUNKS ---")

for i, chunk_item in enumerate(chunks):
    print(f"\n--- Chunk {i + 1} ---")
    print("Length:", len(chunk_item.page_content))
    print(chunk_item.page_content)
    print("Metadata:", chunk_item.metadata)


# 4. Store chunks in ChromaDB
db = vector_store_db(chunks)
resume_docs = db.get(
    where={"resume_id": 101}
)

print("Chunks for resume 101:", len(resume_docs["ids"]))

print("\nVectors successfully stored in ChromaDB!")
print("Stored documents:", db._collection.count())


# 5. Test retrieval with different queries
queries = [
    "Backend development and REST API experience",
    "Frontend development using React and Angular",
    "AI and machine learning projects",
    "Database management using PostgreSQL and MongoDB"
]

print("\n--- RETRIEVAL TESTS ---")

for query in queries:

    print(f"\n--- Query: {query} ---")

    results = retrieve_chunks(
        query=query,
        resume_id=101,
        k=3
    )

    for i, result in enumerate(results):
        print(f"\nChunk {i + 1}")
        print(result.page_content)
        print("Metadata:", result.metadata)


# 6. Test Gemini analysis
job_description = """
We are looking for a Python Backend Developer
with experience in FastAPI, REST APIs,
PostgreSQL and React.

The candidate should have experience building
backend services and integrating APIs.
"""


analysis = analyze_resume(
    resume_id=101,
    job_description=job_description
)


# 7. Display final structured analysis
print("\n--- FINAL RESUME ANALYSIS ---")

print(analysis.model_dump_json(indent=2))
