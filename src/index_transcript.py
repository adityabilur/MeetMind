from src.chunking import chunk_transcript
from src.vector_store import clear_collection, add_documents


with open(
    "data/output/transcript_with_timestamps.txt",
    "r",
    encoding="utf-8"
) as file:
    transcript = file.read()


chunks = chunk_transcript(transcript, chunk_size=5)

clear_collection()

documents = [
    chunk["text"]
    for chunk in chunks
]

ids = [
    f"meeting_chunk_{i}"
    for i in range(len(chunks))
]

metadatas = [
    {
        "start_time": chunk["start_time"],
        "end_time": chunk["end_time"]
    }
    for chunk in chunks
]

add_documents(
    documents,
    ids,
    metadatas
)

print("Transcript indexed successfully!")
print("Number of chunks:", len(chunks))