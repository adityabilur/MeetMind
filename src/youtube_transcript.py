from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url):
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]

    if "youtube.com/watch?v=" in url:
        return url.split("v=")[1].split("&")[0]

    raise ValueError("Invalid YouTube URL")


def get_youtube_transcript(url):
    video_id = extract_video_id(url)

    api = YouTubeTranscriptApi()

    transcript = api.fetch(video_id)

    lines = []

    for entry in transcript:
        start = entry.start
        duration = entry.duration
        end = start + duration

        start_minutes = int(start // 60)
        start_seconds = int(start % 60)

        end_minutes = int(end // 60)
        end_seconds = int(end % 60)

        start_time = f"{start_minutes:02d}:{start_seconds:02d}"
        end_time = f"{end_minutes:02d}:{end_seconds:02d}"

        text = entry.text.strip()

        lines.append(
            f"[{start_time} - {end_time}] {text}"
        )

    return "\n".join(lines)