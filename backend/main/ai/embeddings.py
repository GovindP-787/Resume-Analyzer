from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')


sentences = [
    "Built REST APIs using FastAPI and Python.",
    "Developed backend endpoints with Python.",
    "Designed a logo using Photoshop."
]
embeddings = model.encode(sentences)  
similarity_matrix = cosine_similarity(embeddings)

print("Similarity Matrix:")
print(similarity_matrix)

for i in range(len(sentences)):
    for j in range(i + 1, len(sentences)):
        score = similarity_matrix[i][j]

        print(f"\nSentence 1: {sentences[i]}")
        print(f"Sentence 2: {sentences[j]}")
        print(f"Similarity: {score:.4f}")
