from gemini_client import generate_text
from config import settings


_local_pipeline = None


def _load_local_model():
    global _local_pipeline
    if _local_pipeline is None:
        try:
            from transformers import pipeline
        except ImportError as exc:
            raise RuntimeError(
                "Local explanation mode requires the optional transformers/torch dependencies."
            ) from exc
        _local_pipeline = pipeline(
            "text2text-generation",
            model=settings.local_explanation_model,
        )
    return _local_pipeline


async def explain_concept(topic: str) -> str:
    if settings.use_local_explanation:
        pipe = _load_local_model()
        prompt = (
            "Explain the following educational concept in simple language for a beginner. "
            "Use a short definition, a simple example, and a brief takeaway.\n\n"
            f"Concept: {topic}"
        )
        result = pipe(prompt, max_new_tokens=220, do_sample=False)
        return result[0]["generated_text"].strip()

    prompt = f"""
You are EduGenie, an expert educational explainer.

Explain this concept to a beginner:
{topic}

Use this structure:
- Simple definition
- How it works
- Easy example or analogy
- Key takeaway

Avoid unnecessary jargon. If technical terminology is essential, define it.
"""
    return await generate_text(prompt)
