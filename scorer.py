import nltk
from nltk.corpus import wordnet
from typing import Dict
from app.keyword_extractor import extract_keywords

# Download WordNet data (one-time, runs silently after first download)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)


def get_synonyms(word: str) -> set:
    """Return a set of synonyms for a word using WordNet."""
    synonyms = set()
    for synset in wordnet.synsets(word):
        for lemma in synset.lemmas():
            synonym = lemma.name().replace("_", " ").lower()
            synonyms.add(synonym)
    return synonyms


def is_keyword_matched(keyword: str, student_tokens: set) -> bool:
    """Check exact match first, then synonym match."""
    if keyword in student_tokens:
        return True

    synonyms = get_synonyms(keyword)
    if synonyms & student_tokens:
        return True

    return False


def score_answer(
    reference_answer: str,
    student_answer: str,
    max_score: int = 10
) -> Dict:
    """
    Score a student's answer against a reference answer using
    keyword extraction + exact/synonym matching.
    """

    # Edge case: empty reference
    if not reference_answer.strip():
        return {
            "score": 0, "max_score": max_score, "percentage": 0.0,
            "matched": [], "missed": [], "total_keywords": 0,
            "feedback": "Reference answer was empty."
        }

    ref_keywords = extract_keywords(reference_answer)

    if not ref_keywords:
        return {
            "score": 0, "max_score": max_score, "percentage": 0.0,
            "matched": [], "missed": [], "total_keywords": 0,
            "feedback": "No keywords could be extracted from the reference answer."
        }

    # Tokens from student answer (lemmatised + raw words)
    student_keywords = set(extract_keywords(student_answer))
    raw_student_words = set(student_answer.lower().split())
    student_tokens = student_keywords | raw_student_words

    matched = []
    missed = []

    for keyword in ref_keywords:
        if is_keyword_matched(keyword, student_tokens):
            matched.append(keyword)
        else:
            missed.append(keyword)

    total = len(ref_keywords)
    ratio = len(matched) / total
    raw_score = ratio * max_score
    final_score = round(raw_score)
    percentage = round(ratio * 100, 2)

    if percentage == 100:
        feedback = "Excellent! All keywords matched perfectly."
    elif percentage >= 75:
        feedback = f"Good answer! You missed: {', '.join(missed)}."
    elif percentage >= 50:
        feedback = f"Average answer. Try to include: {', '.join(missed)}."
    else:
        feedback = f"Needs improvement. Important missing concepts: {', '.join(missed)}."

    return {
        "score": final_score,
        "max_score": max_score,
        "percentage": percentage,
        "matched": matched,
        "missed": missed,
        "total_keywords": total,
        "feedback": feedback
    }