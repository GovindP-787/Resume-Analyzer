from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from ai.chunking import chunking

model = SentenceTransformer('all-MiniLM-L6-v2')

def retrieve_chunks(query: str, document: str, chunk_size: int = 300, overlap: int = 70, top_k: int = 2):
    #chunking the document into smaller pieces of texts
    chunks = chunking(document, chunk_size=chunk_size, overlap=overlap)

    #query embedding
    query_embedding = model.encode([query])

    #document embeddings
    document_embeddings = model.encode(chunks)

    #calculating similarity between query and document embeddings
    similarity = cosine_similarity(query_embedding, document_embeddings)[0]
    ranked_indices = similarity.argsort()[::-1]
    results = []
    for i in ranked_indices[:top_k]:
        results.append({
            "chunk": chunks[i],
            "score": float(similarity[i])
        })
    return results

# if __name__ == "__main__":

#     resume_text = """
#     Developed REST APIs using Python and FastAPI.
#     Integrated PostgreSQL databases and implemented CRUD operations.
#     Used Git and GitHub for version control.

#     Built responsive frontend applications using React and TypeScript.
#     Created reusable UI components and integrated backend APIs.

#     Worked on computer vision projects using OpenCV and YOLO.
#     Explored machine learning models and image processing.
#     """

#     job_description = """
#     We need a Python developer with experience in FastAPI,
#     PostgreSQL, REST APIs, and backend development.
#     """

#     results = retrieve_chunks(job_description, resume_text, chunk_size=100, overlap=20, top_k=2)
#     for i, result in enumerate(results, start=1):
#         print(f"\n--- Result {i} ---")
#         print(f"Similarity score: {result['score']:.4f}")
#         print(result["chunk"])