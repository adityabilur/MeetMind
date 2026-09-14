from src.transcription import transcribe_audio


audio_path = "data/input/youtube_audio.m4a"

output_path = "data/output/youtube_transcript.txt"


transcribe_audio(
    audio_path,
    output_path
)


print("YouTube transcription completed!")
print("Transcript saved to:", output_path)