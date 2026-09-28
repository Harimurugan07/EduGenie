from functools import lru_cache

from config import settings


class LocalModelUnavailable(RuntimeError):
    pass


@lru_cache(maxsize=1)
def _load_pipeline():
    if not settings.local_explanation_enabled:
        raise LocalModelUnavailable(
            "Local explanation is disabled. Set LOCAL_EXPLANATION_ENABLED=true."
        )

    try:
        from transformers import pipeline
    except ImportError as exc:
        raise LocalModelUnavailable(
            "Transformers is not installed. Install requirements.txt for local mode."
        ) from exc

    try:
        return pipeline(
            "text2text-generation",
            model=settings.local_explanation_model,
            device=-1,
        )
    except Exception as exc:
        raise LocalModelUnavailable(
            f"Could not load local model '{settings.local_explanation_model}': {exc}"
        ) from exc


def explain_locally(topic: str) -> str:
    generator = _load_pipeline()
    prompt = (
        "Explain the following educational concept to a beginner. "
        "Use simple language, short paragraphs, and one concrete example. "
        "Avoid unnecessary jargon.\n\n"
        f"Concept: {topic}"
    )
    try:
        result = generator(
            prompt,
            max_new_tokens=settings.local_model_max_new_tokens,
            do_sample=False,
        )
        if not result or "generated_text" not in result[0]:
            raise LocalModelUnavailable("Local model returned no explanation.")
        return result[0]["generated_text"].strip()
    except Exception as exc:
        raise LocalModelUnavailable(f"Local explanation failed: {exc}") from exc
