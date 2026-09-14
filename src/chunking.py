def chunk_transcript(transcript, chunk_size=5):
    lines = transcript.splitlines()

    chunks = []

    for i in range(0, len(lines), chunk_size):
        chunk_lines = lines[i:i + chunk_size]

        if not chunk_lines:
            continue

        chunk = "\n".join(chunk_lines)

        first_line = chunk_lines[0]
        last_line = chunk_lines[-1]

        start_time = first_line.split("]")[0].replace("[", "").split(" - ")[0]
        end_time = last_line.split("]")[0].replace("[", "").split(" - ")[1]

        chunks.append({
            "text": chunk,
            "start_time": start_time,
            "end_time": end_time
        })

    return chunks