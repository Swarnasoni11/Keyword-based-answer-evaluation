import spacy
from typing import List

# Load spaCy English model once
# First run: python -m spacy download en_core_web_sm
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    raise OSError(
        "spaCy model not found. Run:  python -m spacy download en_core_web_sm"
    )

# Parts-of-speech considered "meaningful"
MEANINGFUL_POS = {"NOUN", "PROPN", "VERB", "ADJ"}


def extract_keywords(text: str) -> List[str]:
    """
    Extract meaningful, lemmatised, lowercase keywords from text.
    Skips stopwords and punctuation.
    """
    doc = nlp(text.lower())

    keywords = []
    seen = set()

    for token in doc:
        if (
            token.pos_ in MEANINGFUL_POS
            and not token.is_stop
            and not token.is_punct
            and len(token.lemma_) > 1
        ):
            lemma = token.lemma_.lower()
            if lemma not in seen:
                keywords.append(lemma)
                seen.add(lemma)

    return keywords