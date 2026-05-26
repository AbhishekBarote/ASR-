import time

from faster_whisper import WhisperModel

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

def transcribe_with_local_whisper(audio_path):

    start = time.time()

    segments, info = model.transcribe(
        audio_path,
        beam_size=5,
        language="hi",
        task="transcribe"
    )

    transcript = ""

    for segment in segments:
        transcript += segment.text + " "

    latency = time.time() - start

    transcript = transcript.strip()

    return transcript, latency