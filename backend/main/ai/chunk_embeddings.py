from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from ai.chunking import chunking

model = SentenceTransformer('all-MiniLM-L6-v2')

resume_text = """
Python developer experienced in FastAPI and PostgreSQL.
Built REST APIs and integrated databases.
Developed React applications using TypeScript.
Worked on machine learning and computer vision projects.
"""
chunks = chunking(resume_text, chunk_size=100, overlap=20)
print("Resume length:", len(resume_text))
print("Chunk size:", 100)
print("Chunks generated:", len(chunks))
print("Chunk lengths:", [len(chunk) for chunk in chunks])

embedding = model.encode(chunks)

print("length of chunks:", len(chunks))
print("Length of embeddings:", len(embedding))
print("Shape of embeddings:", embedding.shape)

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i + 1}:")
    print(chunk)
    print("Embedding:", embedding[i][:5])