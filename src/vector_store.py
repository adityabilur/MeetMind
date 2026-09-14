import chromadb


client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="meeting_transcript"
)


def clear_collection():
    global collection

    client.delete_collection(name="meeting_transcript")

    collection = client.create_collection(
        name="meeting_transcript"
    )


def add_documents(documents, ids,metadatas):
    collection.add(
        documents=documents,
        ids=ids,
        metadatas=metadatas

    )


def search_documents(query, n_results=3):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    return results