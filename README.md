# Keyword-Based Answer Evaluation System

An intelligent NLP-powered answer evaluation system that automatically grades student responses by extracting important keywords, performing synonym-aware matching, and generating meaningful feedback.

This project demonstrates how AI and Natural Language Processing can be used to automate grading systems for adaptive learning platforms, online exams, and assessment tools.

---

# Project Overview

Traditional grading systems often rely on exact word matching, which can reduce marks even when students explain the correct concept using different words.

This project introduces an intelligent evaluation engine that analyzes the meaning of answers using NLP techniques.

The system:

* Extracts important keywords from reference answers
* Evaluates student responses
* Matches keywords with synonyms
* Calculates answer score
* Generates improvement feedback

---

# Objectives

* Build an automated answer evaluation system
* Implement NLP-based keyword extraction
* Support synonym-aware answer checking
* Create a scalable evaluation API
* Provide meaningful feedback to learners

---

# Features

## Keyword Extraction

Extracts important concepts from reference answers using:

* Tokenization
* POS tagging
* Stopword removal
* Lemmatization

Supported keywords:

* Nouns
* Proper nouns
* Verbs
* Adjectives

---

## Synonym Matching

Uses NLP-based synonym matching to understand different word usage.

Example:

```
car = automobile = vehicle
```

Students receive credit for using similar meanings instead of exact words.

---

## Answer Evaluation

Evaluates answers using:

* Keyword coverage
* Synonym similarity
* Concept matching

Score calculation:

```
Score =
(Matched Keywords / Total Keywords) × Maximum Score
```

---

## Feedback Generation

Provides detailed evaluation feedback.

Example:

```
Score: 7/10

Matched:
- plant
- sunlight
- oxygen

Missing:
- carbon dioxide
- glucose

Suggestion:
Include missing concepts for a better score.
```

---

## Batch Evaluation

Supports evaluating multiple student answers together.

Useful for:

* Online exams
* Assignment checking
* Learning platforms

---

# System Architecture

```
Client
  ↓
FastAPI Endpoint
  ↓
Request Validation
(Pydantic)
  ↓
Keyword Extraction
(spaCy)
  ↓
Synonym Matcher
(WordNet)
  ↓
Scoring Engine
  ↓
Feedback Generator
  ↓
JSON Response
```

---

# Project Structure

```
keyword-answer-evaluation/

│
├── app/
│   │
│   ├── main.py
│   ├── models.py
│   ├── scorer.py
│   ├── keyword_extractor.py
│
├── tests/
│   │
│   ├── test_scorer.py
│   ├── test_api.py
│
├── data/
│   └── sample_qa.json
│
├── requirements.txt
│
└── README.md
```

---

# Technologies Used

| Category         | Technology   |
| ---------------- | ------------ |
| Programming      | Python       |
| API Framework    | FastAPI      |
| Server           | Uvicorn      |
| NLP Processing   | spaCy        |
| Synonym Matching | NLTK WordNet |
| Validation       | Pydantic     |
| Testing          | PyTest       |

---

# Evaluation Logic

The evaluation engine controls how answers are scored.

## Keyword Extraction

```
Reference Answer
        ↓
Text Processing
        ↓
Extract Keywords
        ↓
Create Keyword List
```

---

## Matching Process

```
Student Answer
        ↓
Check Keyword Match
        ↓
Check Synonyms
        ↓
Mark Matched / Missed
        ↓
Calculate Score
```

---

# Evaluation Methods

## Method 1: Exact Keyword Matching

Checks whether important keywords exist directly in the student's answer.

Example:

Reference:

```
Machine learning uses data to train models
```

Student:

```
Machine learning trains models using data
```

Result:

```
Keywords Matched ✓
```

---

## Method 2: Synonym Matching

Uses WordNet to find similar meanings.

Example:

```
automobile → car → vehicle
```

This improves fairness in grading.

---

# API Endpoints

## Health Check

### GET `/`

Response:

```json
{
 "message": "Keyword Answer Evaluation API is running!"
}
```

---

## Evaluate Answer

### POST `/evaluate`

Request:

```json
{
 "reference_answer":
 "Photosynthesis is the process by which plants use sunlight and carbon dioxide to produce glucose",

 "student_answer":
 "Plants use sunlight to make food and release oxygen",

 "max_score":10
}
```

Response:

```json
{
 "score":6,
 "percentage":60,

 "matched_keywords":[
 "plant",
 "sunlight"
 ],

 "missed_keywords":[
 "photosynthesis",
 "glucose"
 ],

 "feedback":
 "Include missing concepts for higher score."
}
```

---

# Edge Cases Handled

| Case                   | Handling            |
| ---------------------- | ------------------- |
| Empty reference answer | Returns score 0     |
| Empty student answer   | All keywords missed |
| No keywords found      | Safe response       |
| Different wording      | Synonym matching    |
| Custom score           | Automatic scaling   |

---

# Sample Workflow

```
Start Evaluation
        ↓
Receive Reference Answer
        ↓
Extract Keywords
        ↓
Analyze Student Answer
        ↓
Match Keywords
        ↓
Check Synonyms
        ↓
Calculate Score
        ↓
Generate Feedback
```

---

# Installation

Clone repository:

```bash
git clone https://github.com/yourusername/keyword-answer-evaluation.git
```

Navigate:

```bash
cd keyword-answer-evaluation
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Download NLP Models

spaCy:

```bash
python -m spacy download en_core_web_sm
```

NLTK:

```python
import nltk

nltk.download("wordnet")
nltk.download("omw-1.4")
```

---

# Run Application

Start server:

```bash
python -m uvicorn app.main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

# Requirements

```
fastapi
uvicorn
pydantic
spacy
nltk
pytest
httpx
```

---

# Future AI Enhancements

* Sentence Transformer based semantic scoring
* Deep learning answer evaluation
* Multi-language support
* Weighted keyword importance
* Teacher analytics dashboard
* Database integration
* AI-based personalized feedback

---

# Learning Outcomes

Through this project you will learn:

* NLP pipeline development
* Keyword extraction techniques
* Text preprocessing
* Lemmatization
* Synonym matching
* REST API development
* AI-based evaluation systems

---

# Author

**Swarna Soni**

AI/ML Enthusiast | Python Developer | Machine Learning Learner

If you find this project useful, consider giving it a ⭐ on GitHub.
