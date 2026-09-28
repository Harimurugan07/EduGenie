from typing import Literal

from pydantic import BaseModel, Field, field_validator


def clean_text(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("Input cannot be empty.")
    return value


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1)

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        return clean_text(value)


class QARequest(BaseModel):
    question: str = Field(..., min_length=1)

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        return clean_text(value)


class ExplainRequest(BaseModel):
    topic: str = Field(..., min_length=1)

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, value: str) -> str:
        return clean_text(value)


class QuizRequest(TextRequest):
    pass


class SummaryRequest(TextRequest):
    pass


class LearningPathRequest(BaseModel):
    topic: str = Field(..., min_length=1)
    level: Literal["beginner", "intermediate", "advanced"] = "beginner"
    weeks: int = Field(default=8, ge=1, le=52)

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, value: str) -> str:
        return clean_text(value)


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str


class QuizResponse(BaseModel):
    title: str
    questions: list[QuizQuestion] = Field(min_length=3, max_length=3)


class LearningPathStep(BaseModel):
    stage: str
    topics: list[str]
    estimated_time: str
    resources: list[str]
    practice: list[str]


class LearningPathResponse(BaseModel):
    topic: str
    learner_level: str
    duration: str
    steps: list[LearningPathStep]
