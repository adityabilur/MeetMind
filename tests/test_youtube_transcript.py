from youtube_transcript_api import YouTubeTranscriptApi


video_id = "3WrZMzqpFTc"

api = YouTubeTranscriptApi()

transcript = api.fetch(video_id)

print("Transcript fetched successfully!")
print("Number of transcript entries:", len(transcript))

for entry in transcript[:5]:
    print(entry)