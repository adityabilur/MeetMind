import yt_dlp


def download_youtube_video(url):

    output_path = "data/input/youtube_audio.%(ext)s"

    options = {
        "format": "140",
        "outtmpl": output_path,
        "noplaylist": True
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

    print("YouTube audio downloaded successfully!")