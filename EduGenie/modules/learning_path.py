from ai.gemini_client import get_gemini_client
from config import settings
from schemas import LearningPathResponse


def get_learning_recommendations(
    topic: str,
    level: str = "beginner",
    weeks: int = 8,
) -> LearningPathResponse:
    if len(topic) > settings.max_learning_topic_chars:
        raise ValueError(
            f"Topic is too long. Maximum is {settings.max_learning_topic_chars} characters."
        )

    prompt = f"""
Create a personalized learning path for the topic "{topic}".

Learner level: {level}
Duration: {weeks} weeks

Requirements:
- Start from concepts appropriate to the learner's level.
- Progress from foundational knowledge toward advanced topics.
- Divide the plan into logical stages.
- Give estimated time for each stage.
- Provide useful resource suggestions as resource names/types or URLs when you know
  reliable public URLs; never fabricate a specific URL.
- Include practical exercises for every stage.
- Keep the plan realistic for self-study.
- Return only data matching the requested structured schema.
"""
    client = get_gemini_client()

    try:
        return client.structured(
            prompt,
            LearningPathResponse,
            temperature=0.35,
        )
    except Exception as e:
        print("GEMINI ERROR:", repr(e))
        raise