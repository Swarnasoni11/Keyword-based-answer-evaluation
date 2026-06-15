from fastapi import FastAPI, HTTPException
from app.models import EvaluationRequest, EvaluationResponse
from app.scorer import score_answer

app = FastAPI(
    title="Keyword-Based Answer Evaluation API",
    description="Scores student answers by matching keywords from a reference answer, with synonym support.",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "Keyword Answer Evaluation API is running!"}


@app.post("/evaluate", response_model=EvaluationResponse)
def evaluate_answer(request: EvaluationRequest):
    try:
        result = score_answer(
            reference_answer=request.reference_answer,
            student_answer=request.student_answer,
            max_score=request.max_score
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scoring failed: {str(e)}")

    return EvaluationResponse(
        score=result["score"],
        max_score=result["max_score"],
        percentage=result["percentage"],
        matched_keywords=result["matched"],
        missed_keywords=result["missed"],
        total_keywords=result["total_keywords"],
        feedback=result["feedback"]
    )


@app.post("/evaluate/batch")
def evaluate_batch(requests: list[EvaluationRequest]):
    results = []
    for req in requests:
        result = score_answer(req.reference_answer, req.student_answer, req.max_score)
        results.append(result)
    return {"results": results, "total_evaluated": len(results)}