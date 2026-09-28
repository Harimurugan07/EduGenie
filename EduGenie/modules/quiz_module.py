from ai.gemini_client import get_gemini_client
from config import settings
from schemas import QuizResponse


def generate_quiz(text: str) -> QuizResponse:
    if len(text) > settings.max_quiz_chars:
        raise ValueError(
            f"Quiz source text is too long. Maximum is {settings.max_quiz_chars} characters."
        )

    prompt = f"""
Create a quiz from the educational passage below.

Requirements:
- Exactly 3 multiple-choice questions.
- Exactly 4 options per question.
- Exactly one correct answer per question.
- The correct_answer field must exactly match one of the four options.
- Distractors should be plausible but clearly incorrect.
- Include a concise explanation for each answer.
- Questions must be answerable from the supplied passage.
- Return only data matching the requested structured schema.

Passage:
{text}
"""
    result = get_gemini_client().structured(prompt, QuizResponse, temperature=0.3)

    for question in result.questions:
        if question.correct_answer not in question.options:
            raise ValueError("AI generated an invalid quiz: correct answer is not an option.")

    return result
