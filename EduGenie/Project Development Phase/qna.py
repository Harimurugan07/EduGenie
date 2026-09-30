from gemini_client import generate_text


async def answer_question(question: str) -> str:
    prompt = f"""
You are EduGenie, a concise educational tutor.

Answer the student's question accurately and clearly.
- Start with the direct answer.
- Explain important reasoning or context.
- Use simple language suitable for a learner.
- If the question is ambiguous, state the assumption you are making.
- Do not invent sources, facts, quotations, or citations.

Student question:
{question}
"""
    return await generate_text(prompt)
