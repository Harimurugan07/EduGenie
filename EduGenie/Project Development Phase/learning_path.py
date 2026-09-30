from gemini_client import generate_text


async def get_learning_recommendations(topic: str) -> str:
    prompt = f"""
You are EduGenie, a personalized learning-path designer.

Create a structured learning path for: {topic}

Assume a beginner unless the learner explicitly states another level.
Organize the plan from beginner to advanced and include:
- Stage and difficulty
- Concepts to learn
- Suggested timeline
- Practice activities/projects
- Resource types to seek (videos, articles, books, documentation)
- A simple milestone/checkpoint for each stage

Keep it practical and adaptable. Do not fabricate specific URLs or claim a resource exists unless you know it.
"""
    return await generate_text(prompt)
