import os
import time

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is not configured."
    )

client = genai.Client(
    api_key=api_key
)


def ask_gemini(prompt, max_retries=3):

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            return response.text

        except Exception as error:

            error_text = str(error)

            # Temporary Gemini server overload.
            if "503" in error_text or "UNAVAILABLE" in error_text:

                if attempt == max_retries - 1:
                    raise

                wait_time = 5 * (2 ** attempt)

                print(
                    f"Gemini temporarily unavailable. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:
                raise