from pydantic import BaseModel, Field
from typing import List, Optional


# ── REQUEST MODEL ──────────────────────────────────────────────
class EvaluationRequest(BaseModel):
    reference_answer: str = Field(
        ...,
        description="The correct / model answer provided by the instructor",
        example="Photosynthesis is the process by which plants use sunlight, water, and carbon dioxide to produce glucose and oxygen."
    )
    student_answer: str = Field(
        ...,
        description="The answer submitted by the student",
        example="Plants use sunlight and water to make food and release oxygen."
    )
    max_score: Optional[int] = Field(
        default=10,
        description="Maximum possible score (default 10)",
        ge=1,
        le=100
    )


# ── RESPONSE MODEL ─────────────────────────────────────────────
class EvaluationResponse(BaseModel):
    score: int = Field(..., description="Score awarded to the student")
    max_score: int = Field(..., description="Maximum possible score")
    percentage: float = Field(..., description="Score as a percentage")
    matched_keywords: List[str] = Field(..., description="Keywords found in student answer")
    missed_keywords: List[str] = Field(..., description="Keywords missing from student answer")
    total_keywords: int = Field(..., description="Total keywords extracted from reference answer")
    feedback: str = Field(..., description="Short feedback message for the student")