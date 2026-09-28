from fastapi import APIRouter, HTTPException

from ai.gemini_client import GeminiConfigurationError, GeminiGenerationError
from ai.local_explainer import LocalModelUnavailable
from modules.explanation_module import explain_concept
from modules.learning_path import get_learning_recommendations
from modules.qna import answer_question
from modules.quiz_module import generate_quiz
from modules.summary_module import summarize_text
from schemas import (
    ExplainRequest,
    LearningPathRequest,
    QuizRequest,
    QuizResponse,
    QARequest,
    SummaryRequest,
)

router = APIRouter()


def _ai_error(exc: Exception) -> HTTPException:
    if isinstance(exc, GeminiConfigurationError):
        return HTTPException(status_code=503, detail=str(exc))
    if isinstance(exc, (GeminiGenerationError, LocalModelUnavailable)):
        return HTTPException(status_code=502, detail=str(exc))
    if isinstance(exc, ValueError):
        return HTTPException(status_code=422, detail=str(exc))
    return HTTPException(status_code=500, detail="Unexpected server error.")


@router.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}


@router.post("/qa")
async def qa(request: QARequest):
    try:
        return {"answer": answer_question(request.question)}
    except Exception as exc:
        raise _ai_error(exc) from exc


@router.post("/explain")
async def explain(request: ExplainRequest):
    try:
        return {"explanation": explain_concept(request.topic)}
    except Exception as exc:
        raise _ai_error(exc) from exc


@router.post("/quiz", response_model=QuizResponse)
async def quiz(request: QuizRequest):
    try:
        return generate_quiz(request.text)
    except Exception as exc:
        raise _ai_error(exc) from exc


@router.post("/summarize")
async def summarize(request: SummaryRequest):
    try:
        return {"summary": summarize_text(request.text)}
    except Exception as exc:
        raise _ai_error(exc) from exc


@router.post("/learn/recommendations")
async def learning_recommendations(request: LearningPathRequest):
    try:
        return get_learning_recommendations(
            request.topic,
            request.level,
            request.weeks,
        )
    except Exception as exc:
        raise _ai_error(exc) from exc
