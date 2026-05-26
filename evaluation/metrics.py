from evaluation.wer import calculate_wer

from fuzzy.fuzzy_score import calculate_fuzzy_score
from fuzzy.locality_fuzzy_match import find_best_locality_match

from evaluation.transliterate import (
    transliterate_to_english
)

from evaluation.normalize import normalize_text


def evaluate_model(
    reference_text,
    transcription,
    expected_locality,
    latency
):

    # Transliterate Hindi script to English-like text
    transcription = transliterate_to_english(
        transcription
    )

    # Normalize text
    transcription = normalize_text(
        transcription
    )

    reference_text = normalize_text(
        reference_text
    )

    expected_locality = normalize_text(
        expected_locality
    )

    # Calculate WER
    wer_score = calculate_wer(
        reference_text,
        transcription
    )

    # Fuzzy locality matching
    predicted_locality, locality_score = (
        find_best_locality_match(transcription)
    )

    # Similarity score
    fuzzy_score = calculate_fuzzy_score(
        expected_locality,
        predicted_locality
    )

    # Accept fuzzy matches
    locality_correct = locality_score >= 62

    return {

        "reference_text": reference_text,

        "transcription": transcription,

        "expected_locality": expected_locality,

        "predicted_locality": predicted_locality,

        "locality_match_score": locality_score,

        "fuzzy_score": fuzzy_score,

        "locality_correct": locality_correct,

        "wer": round(wer_score, 4),

        "latency_seconds": round(latency, 2)
    }