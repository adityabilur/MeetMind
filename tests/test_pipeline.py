from src.pipeline import process_input


url = input("Enter YouTube URL: ")


transcript_path = process_input(
    url,
    "youtube"
)


print("\nTranscript created successfully!")
print("Saved to:", transcript_path)