from src.rag_pipeline import answer_question


question = input("Ask a question about the meeting: ")

answer, sources, metadatas = answer_question(question)

print("\n===== ANSWER =====")
print(answer)

print("\n===== SOURCES =====")

for i, (source, metadata) in enumerate(
    zip(sources, metadatas),
    start=1
):
    print(f"\nSource {i}:")
    print(
        f"Timestamp: {metadata['start_time']} - "
        f"{metadata['end_time']}"
    )
    print(source)