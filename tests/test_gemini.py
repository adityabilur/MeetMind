from src.summarizer import summarize_meeting


with open(
    "data/output/transcript_with_timestamps.txt",
    "r",
    encoding="utf-8"
) as file:
    transcript = file.read()


summary = summarize_meeting(transcript)

print("\n===== MEETING SUMMARY =====\n")
print(summary)