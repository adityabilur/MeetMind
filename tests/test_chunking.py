from src.chunking import chunk_transcript


with open(
    "data/output/transcript_with_timestamps.txt",
    "r",
    encoding="utf-8"
) as file:
    transcript = file.read()


chunks = chunk_transcript(transcript, chunk_size=5)


print("Number of chunks:", len(chunks))

for i, chunk in enumerate(chunks[:3]):
    print(f"\n===== CHUNK {i + 1} =====")
    print(chunk)