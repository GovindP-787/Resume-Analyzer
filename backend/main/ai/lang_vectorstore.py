from lang_embeddings import get_embeddings
from langchain_chroma import Chroma
from pathlib import Path

def vector_store_db(chunks):
    embedding = get_embeddings()
    db_path = Path(__file__).resolve().parent / "chroma_db"

    vector_store = Chroma.from_documents(documents=chunks,persist_directory= str(db_path), embedding=embedding, collection_name="resumate_resumes" )
    return vector_store
