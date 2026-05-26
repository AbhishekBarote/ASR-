from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

def transliterate_to_english(text):

    try:

        converted = transliterate(
            text,
            sanscript.DEVANAGARI,
            sanscript.ITRANS
        )

        return converted.lower()

    except:

        return text.lower()