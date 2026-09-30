from gemini_client import generate_text


async def summarize_text(text: str) -> str:
    prompt = f"""
You are EduGenie, an educational summarizer.

Summarize the passage below for quick revision.
Return:
1. A short overview (2-3 sentences).
2. Key points as bullets.
3. Important terms or concepts, if present.

Preserve the original meaning and do not introduce facts not supported by the passage.

PASSAGE:
{text}
"""
    return await generate_text(prompt)
