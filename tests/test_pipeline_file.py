from src.pipeline import process_input

file_path = "data/input/meeting.mp4"

transcript_path = process_input(
    file_path,
    "file"
)

print("\nTranscript created successfully!")
print("Saved to:", transcript_path)