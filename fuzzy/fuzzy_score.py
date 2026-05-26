from rapidfuzz import fuzz

def calculate_fuzzy_score(expected, predicted):

    if not predicted:
        return 0

    return fuzz.ratio(
        expected.lower(),
        predicted.lower()
    )