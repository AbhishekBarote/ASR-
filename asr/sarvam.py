import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

def transcribe_with_sarvam(audio_path):

    url = "https://api.sarvam.ai/speech-to-text"

    headers = {
        "api-subscription-key": SARVAM_API_KEY
    }

    files = {
        "file": open(audio_path, "rb")
    }

    start = time.time()

    response = requests.post(
        url,
        headers=headers,
        files=files
    )

    latency = time.time() - start

    try:
        result = response.json()
    except:
        result = {}

    transcript = (
        result.get("transcript")
        or result.get("text")
        or ""
    )

    return transcript, latency