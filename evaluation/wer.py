from jiwer import wer

def calculate_wer(reference, hypothesis):

    if not hypothesis:
        return 1.0

    return wer(reference, hypothesis)