import os
import mimetypes
import time

from dotenv import load_dotenv
from deepgram import DeepgramClient, PrerecordedOptions

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

client = DeepgramClient(DEEPGRAM_API_KEY)

def transcribe_with_deepgram(audio_path):

    with open(audio_path, "rb") as audio:
        buffer_data = audio.read()

    mime_type = mimetypes.guess_type(audio_path)[0]

    payload = {
        "buffer": buffer_data,
        "mimetype": mime_type
    }

    options = PrerecordedOptions(
        model="nova-3",
        smart_format=True,
        language="hi"
    )

    start = time.time()

    response = client.listen.prerecorded.v("1").transcribe_file(
        payload,
        options
    )

    latency = time.time() - start

    transcript = (
        response.results.channels[0]
        .alternatives[0]
        .transcript
    )

    return transcript, latency