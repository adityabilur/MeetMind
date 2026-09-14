import whisper


model = whisper.load_model("base")


def transcribe_audio(audio_path, output_path):
    result = model.transcribe(audio_path)

    with open(output_path, "w", encoding="utf-8") as file:
        for segment in result["segments"]:

            start = format_time(segment["start"])
            end = format_time(segment["end"])
            text = segment["text"].strip()

            file.write(f"[{start} - {end}] {text}\n")

    return result


def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)

    return f"{minutes:02d}:{seconds:02d}"