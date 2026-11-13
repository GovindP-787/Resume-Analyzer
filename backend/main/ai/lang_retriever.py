from lang_vectorstore import vector_store_db
from lang_embeddings import get_embeddings
from pathlib import Path
from langchain_chroma import Chroma

def load_vector_store():
    model = get_embeddings()
    db_path = Path(__file__).resolve().parent / "chroma_db"
    db = Chroma(collection_name="resumate_resumes",
                embedding_function=model,
                persist_directory=str(db_path))
    return db

def retrieve_chunks(query: str, resume_id: int, k: int = 3):
    db = load_vector_store()
    result = db.similarity_search(
        query = query,
        k = k,
        filter={"resume_id": resume_id}

    )
    return result