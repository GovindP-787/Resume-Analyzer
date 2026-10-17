from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_search(query: str, documents: list[str], top_k: int = 2):
    query_embedding = model.encode([query])
    document_embeddings = model.encode(documents)
    similarity = cosine_similarity(query_embedding, document_embeddings)[0]
    ranked_indices = similarity.argsort()[::-1]
    results = []

    for index in ranked_indices[:top_k]:
        results.append({
            "document": documents[index],
            "score": float(similarity[index])
        })

    return results


documents = [
    "Built REST APIs using Python and FastAPI.",
    "Designed a responsive portfolio using React and CSS.",
    "Created PostgreSQL tables and SQL queries.",
    "Developed a machine learning model using Python.",
    "Designed logos and marketing graphics using Photoshop."
]

query = "Experience with Python backend development"

results = semantic_search(query, documents)

for result in results:
    print(f"\nScore: {result['score']:.4f}")
    print(f"Document: {result['document']}")
