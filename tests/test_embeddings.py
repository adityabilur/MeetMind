from src.embeddings import create_embedding


text = "The project deadline is September 20."

embedding = create_embedding(text)

print("Embedding created!")
print("Number of values:", len(embedding))
print("First 10 values:", embedding[:10])