from lang_splitter import split_resume
from lang_embeddings import get_embeddings
from lang_document import create_langchain_document
from lang_vectorstore import vector_store_db
from lang_retriever import retrieve_chunks



text = """
Python developer with experience in FastAPI and PostgreSQL.
Developed React applications and worked with REST APIs.
"""

doc = create_langchain_document(resume_text = text, resume_id= 100, file_name= "test.pdf")
chunk = split_resume(doc)

# for i,chunk in enumerate(chunk):
#     print(f"\nChunk {i + 1}")
#     print(chunk.page_content)
#     print(chunk.metadata)

# chunk_embedding = get_embeddings()
# chunk_texts = [chunk.page_content for chunk in chunk]
# vectors = chunk_embedding.embed_documents(chunk_texts)
# for i, vector in enumerate(vectors):
#     print(f"\nChunk {i + 1}")
#     print("Vector dimensions:", len(vector))
#     print("First 5 values:", vector[:5])

db = vector_store_db(chunk)
print("Vectors successfully stored in ChromaDB!")
print("Stored documents:", db._collection.count())

query = """
Looking for a Python backend developer with experience
in FastAPI, PostgreSQL and REST APIs.
"""

result = retrieve_chunks(query=query, resume_id=100, k=3)
print("\n--- Retrieved Results ---")

for i, result in enumerate(result):
    print(f"\nChunk {i + 1}")
    print(result.page_content)
    print(result.metadata)



