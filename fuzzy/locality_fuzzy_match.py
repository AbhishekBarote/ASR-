from rapidfuzz import fuzz

from data.bangalore_localities import (
    BANGALORE_LOCALITIES
)


def find_best_locality_match(text):

    if not text:
        return None, 0

    text = text.lower()

    best_locality = None
    best_score = 0

    for locality in BANGALORE_LOCALITIES:

        locality_lower = locality.lower()

        # Full phrase similarity
        full_score = fuzz.partial_ratio(
            text,
            locality_lower
        )

        # Token similarity boost
        locality_tokens = locality_lower.split()

        token_boost = 0

        for token in locality_tokens:

            if token in text:
                token_boost += 20

        final_score = full_score + token_boost

        if final_score > best_score:

            best_score = final_score
            best_locality = locality

    return best_locality, min(best_score, 100)