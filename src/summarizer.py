from src.gemini_service import ask_gemini


def summarize_meeting(transcript):

    prompt = f"""
You are MeetMind, an AI audio and video intelligence assistant.

Analyze the following transcript.

Provide the output in these sections:

1. Summary
2. Key Discussion Points
3. Important Information
4. Decisions or Conclusions
5. Action Items

If a section is not relevant to the content, clearly mention:
"Not applicable."

Keep the response clear, concise, and useful.

Transcript:
{transcript}
"""

    return ask_gemini(prompt)