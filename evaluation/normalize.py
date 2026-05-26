import re

def normalize_text(text):

    if not text:
        return ""

    text = text.lower()

    text = re.sub(
        r"[^a-zA-Z0-9\s]",
        "",
        text
    )

    # locality normalization
    text = text.replace(
        "kura mangala",
        "koramangala"
    )

    text = text.replace(
        "kora mangla",
        "koramangala"
    )

    text = text.replace(
        "silco",
        "silk"
    )

    text = text.replace(
        "silkho",
        "silk"
    )

    return text.strip()