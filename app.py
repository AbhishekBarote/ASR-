import os
import pandas as pd

from asr.deepgram import transcribe_with_deepgram
from asr.whisper_groq import transcribe_with_groq
from asr.local_whisper import transcribe_with_local_whisper
from asr.sarvam import transcribe_with_sarvam

from evaluation.metrics import evaluate_model

RECORDINGS_DIR = "recordings"

ground_truth = {

    "001_koramangala.wav": {
        "locality": "Koramangala",
        "reference": "Haan main Koramangala mein rehta hoon"
    },

    "002_silk_board.wav": {
        "locality": "Silk Board",
        "reference": "Main Silk Board ke paas rehta hoon"
    },

    "003_white_field.wav": {
        "locality": "Whitefield",
        "reference": "Main Whitefield side kaam karta hoon"
    },

    "004_Kothanur_Dinne.wav": {
        "locality": "Kothanur Dinne",
        "reference": "Haan main Kothanur Dinne mein rehta hoon"
    },
        "006_indiranagar.wav": {
        "locality": "Indiranagar",
        "reference": "Mera office Indiranagar side hai"
    },

    "007_jayanagar.wav": {
        "locality": "Jayanagar",
        "reference": "Haan main Jayanagar mein rehta hoon"
    },

    "008_majestic.wav": {
        "locality": "Majestic",
        "reference": "Main Majestic bus stand ke paas hoon"
    },

    "009_rajajinagar.wav": {
        "locality": "Rajajinagar",
        "reference": "Mera office Rajajinagar mein hai"
    },

    "010_bellandur.wav": {
        "locality": "Bellandur",
        "reference": "Haan main Bellandur mein rehta hoon"
    },

    "011_hebbal.wav": {
        "locality": "Hebbal",
        "reference": "Main Hebbal side kaam karta hoon"
    },

    "012_yelahanka.wav": {
        "locality": "Yelahanka",
        "reference": "Mera ghar Yelahanka mein hai"
    },

    "013_kr_puram.wav": {
        "locality": "KR Puram",
        "reference": "Haan main KR Puram mein rehta hoon"
    },

    "014_sarjapur.wav": {
        "locality": "Sarjapur",
        "reference": "Main Sarjapur road ke paas rehta hoon"
    },

    "015_peenya.wav": {
        "locality": "Peenya",
        "reference": "Mera factory Peenya side hai"
    },

    "016_yeshwanthpur.wav": {
        "locality": "Yeshwanthpur",
        "reference": "Haan main Yeshwanthpur mein rehta hoon"
    },

    "017_banashankari.wav": {
        "locality": "Banashankari",
        "reference": "Main Banashankari side rehta hoon"
    },

    "018_marathahalli.wav": {
        "locality": "Marathahalli",
        "reference": "Mera office Marathahalli mein hai"
    },

    "019_thanisandra.wav": {
        "locality": "Thanisandra",
        "reference": "Haan main Thanisandra mein rehta hoon"
    },

    "020_electronic_city.wav": {
        "locality": "Electronic City",
        "reference": "Main Electronic City side kaam karta hoon"
    }
}

models = {
    "Deepgram_Nova3": transcribe_with_deepgram,
    "Groq_Whisper_Large": transcribe_with_groq,
    "Whisper_Small_Local": transcribe_with_local_whisper,
    "Sarvam_AI": transcribe_with_sarvam
}

results = []

for file_name in os.listdir(RECORDINGS_DIR):

    SUPPORTED_FORMATS = (
        ".wav",
        ".mp3",
        ".m4a",
        ".flac",
        ".ogg"
    )

    if not file_name.lower().endswith(SUPPORTED_FORMATS):
        continue

    if file_name not in ground_truth:
        print(f"Ground truth missing for {file_name}")
        continue

    audio_path = os.path.join(
        RECORDINGS_DIR,
        file_name
    )

    expected_locality = (
        ground_truth[file_name]["locality"]
    )

    reference_text = (
        ground_truth[file_name]["reference"]
    )

    for model_name, model_function in models.items():

        print(f"\nRunning {model_name} on {file_name}")

        try:

            transcription, latency = model_function(
                audio_path
            )

            metrics = evaluate_model(
                reference_text=reference_text,
                transcription=transcription,
                expected_locality=expected_locality,
                latency=latency
            )

            metrics["model"] = model_name
            metrics["audio_file"] = file_name

            results.append(metrics)

            print("Transcription:", transcription)

        except Exception as e:

            print(f"Error with {model_name}")
            print(e)

df = pd.DataFrame(results)

os.makedirs("reports", exist_ok=True)

excel_path = "reports/asr_benchmark_results.xlsx"

df.to_excel(
    excel_path,
    index=False
)

print("\nBenchmark completed successfully.")
print(f"Saved report to: {excel_path}")

summary = df.groupby("model").agg({
    "wer": "mean",
    "fuzzy_score": "mean",
    "latency_seconds": "mean",
    "locality_correct": "mean"
})

print("\nModel Summary:")
print(summary)