from src.vector_store import add_documents, search_documents


documents = [
    "The team discussed the project timeline.",
    "The final project deadline was set for September 20.",
    "Rahul will prepare the presentation.",
    "The next meeting will be held on Monday."
]

ids = [
    "chunk_1",
    "chunk_2",
    "chunk_3",
    "chunk_4"
]


add_documents(documents, ids)

results = search_documents(
    "When is the project deadline?"
)

print(results)