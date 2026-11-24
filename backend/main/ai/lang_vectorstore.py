from .lang_embeddings import get_embeddings
from langchain_chroma import Chroma
from pathlib import Path


def vector_store_db(chunks):
    embedding = get_embeddings()

    db_path = Path(__file__).resolve().parent / "chroma_db"

    vector_store = Chroma(
        collection_name="resumate_resumes",
        persist_directory=str(db_path),
        embedding_function=embedding
    )

    if not chunks:
        return vector_store

    # Get the resume ID from the document metadata
    resume_id = chunks[0].metadata["resume_id"]

    # Delete previously indexed chunks for this resume
    vector_store.delete(
        where={"resume_id": resume_id}
    )

    # Generate stable IDs for the new chunks
    ids = [
        f"{resume_id}_{i}"
        for i in range(len(chunks))
    ]

    # Store the updated chunks
    vector_store.add_documents(
        documents=chunks,
        ids=ids
    )

    return vector_store