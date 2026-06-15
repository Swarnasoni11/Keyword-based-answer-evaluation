import pytest
from app.scorer import score_answer, get_synonyms, is_keyword_matched
from app.keyword_extractor import extract_keywords


class TestKeywordExtractor:

    def test_extracts_nouns(self):
        keywords = extract_keywords("The dog chases the ball")
        assert "dog" in keywords or "chase" in keywords

    def test_removes_stopwords(self):
        keywords = extract_keywords("The cat is a small animal")
        assert "the" not in keywords
        assert "is" not in keywords
        assert "a" not in keywords

    def test_lemmatisation(self):
        keywords = extract_keywords("Plants are producing oxygen")
        assert "plant" in keywords or "produce" in keywords

    def test_empty_string(self):
        keywords = extract_keywords("")
        assert keywords == []


class TestGetSynonyms:

    def test_car_synonyms(self):
        syns = get_synonyms("car")
        assert "automobile" in syns or "auto" in syns

    def test_unknown_word(self):
        syns = get_synonyms("xyzabc123")
        assert isinstance(syns, set)

    def test_returns_set(self):
        syns = get_synonyms("happy")
        assert isinstance(syns, set)


class TestScoreAnswer:

    def test_perfect_answer(self):
        ref = "Photosynthesis uses sunlight water and carbon dioxide"
        student = "Photosynthesis uses sunlight water and carbon dioxide"
        result = score_answer(ref, student, max_score=10)
        assert result["score"] == 10
        assert result["percentage"] == 100.0

    def test_empty_student_answer(self):
        result = score_answer("Plants produce oxygen", "", max_score=10)
        assert result["score"] == 0

    def test_empty_reference_answer(self):
        result = score_answer("", "Some student answer", max_score=10)
        assert result["score"] == 0

    def test_partial_answer(self):
        ref = "Photosynthesis uses sunlight water carbon dioxide glucose oxygen"
        student = "Plants use sunlight and water"
        result = score_answer(ref, student, max_score=10)
        assert 0 < result["score"] < 10

    def test_synonym_matching(self):
        ref = "The automobile moves fast"
        student = "The car moves quickly"
        result = score_answer(ref, student, max_score=10)
        assert result["score"] > 0

    def test_score_does_not_exceed_max(self):
        ref = "water oxygen glucose sunlight"
        student = "water oxygen glucose sunlight carbon"
        result = score_answer(ref, student, max_score=10)
        assert result["score"] <= 10

    def test_feedback_excellent(self):
        ref = "oxygen water"
        student = "oxygen water"
        result = score_answer(ref, student)
        assert "Excellent" in result["feedback"]

    def test_matched_and_missed_lists(self):
        ref = "photosynthesis sunlight water carbon dioxide glucose"
        student = "sunlight water glucose"
        result = score_answer(ref, student, max_score=10)
        assert len(result["matched"]) + len(result["missed"]) == result["total_keywords"]

    def test_custom_max_score(self):
        ref = "oxygen carbon"
        student = "oxygen carbon"
        result = score_answer(ref, student, max_score=20)
        assert result["score"] == 20
        assert result["max_score"] == 20