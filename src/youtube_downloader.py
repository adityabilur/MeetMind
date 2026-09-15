import os
import uuid

import yt_dlp


def download_youtube_video(url):

    

    os.makedirs("data/input", exist_ok=True)

    file_id = uuid.uuid4().hex
    output_path = f"data/input/youtube_{file_id}.%(ext)s"

    options = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        downloaded_path = ydl.prepare_filename(info)

    print("YouTube audio downloaded successfully!")
    print("Downloaded file:", downloaded_path)

    return downloaded_path