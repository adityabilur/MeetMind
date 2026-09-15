import os

from src.youtube_downloader import download_youtube_video
from src.transcription import transcribe_audio
from src.chunking import chunk_transcript
from src.vector_store import clear_collection, add_documents


def process_input(input_value, input_type):

    # -----------------------------
    # Step 1: Get the audio/media
    # -----------------------------
    os.makedirs("data/input", exist_ok=True)
    os.makedirs("data/output", exist_ok=True)
    if input_type == "youtube":

        print("Downloading YouTube audio...")

        audio_path = download_youtube_video(input_value)
    elif input_type == "file":

        audio_path = input_value

        if not os.path.exists(audio_path):
            raise FileNotFoundError(
                f"File not found: {audio_path}"
            )

    else:

        raise ValueError(
            "input_type must be 'youtube' or 'file'"
        )

    # -----------------------------
    # Step 2: Transcribe
    # -----------------------------

    transcript_path = "data/output/transcript.txt"

    print("Starting transcription...")

    transcribe_audio(
        audio_path,
        transcript_path
    )

    print("Transcription completed!")

    # -----------------------------
    # Step 3: Read transcript
    # -----------------------------

    with open(
        transcript_path,
        "r",
        encoding="utf-8"
    ) as file:
        transcript = file.read()

    # -----------------------------
    # Step 4: Create chunks
    # -----------------------------

    chunks = chunk_transcript(
        transcript,
        chunk_size=5
    )

    print("Number of chunks:", len(chunks))

    # -----------------------------
    # Step 5: Clear old meeting
    # -----------------------------

    clear_collection()

    # -----------------------------
    # Step 6: Prepare ChromaDB data
    # -----------------------------

    documents = [
        chunk["text"]
        for chunk in chunks
    ]

    ids = [
        f"meeting_chunk_{i}"
        for i in range(len(chunks))
    ]

    metadatas = [
        {
            "start_time": chunk["start_time"],
            "end_time": chunk["end_time"]
        }
        for chunk in chunks
    ]

    # -----------------------------
    # Step 7: Store in ChromaDB
    # -----------------------------

    add_documents(
        documents,
        ids,
        metadatas
    )

    print("Transcript indexed successfully!")

    return transcript_path