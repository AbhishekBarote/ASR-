import os
import time

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def transcribe_with_groq(audio_path):

    start = time.time()

    with open(audio_path, "rb") as file:

        response = client.audio.transcriptions.create(
            file=file,
            model="whisper-large-v3",
            language="en",
            prompt=(
                "The audio contains Indian locality names "
                "spoken in Hinglish. "
                "Transcribe using English alphabets only."
            ),
            response_format="verbose_json"
        )

    latency = time.time() - start

    return response.text, latency