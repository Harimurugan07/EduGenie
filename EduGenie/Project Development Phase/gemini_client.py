from config import settings

_client = None


def get_client():
    global _client
    if _client is None:
        if not settings.gemini_api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured. Create a Gemini API key and add it to .env."
            )
        try:
            from google import genai
        except ImportError as exc:
            raise RuntimeError(
                "The Google Gemini SDK is not installed. Run: pip install -r requirements.txt"
            ) from exc
        _client = genai.Client(api_key=settings.gemini_api_key)
    return _client


async def generate_text(prompt: str, *, temperature: float | None = None,
                        max_output_tokens: int | None = None) -> str:
    from google.genai import types

    client = get_client()
    response = await client.aio.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=settings.temperature if temperature is None else temperature,
            max_output_tokens=(
                settings.max_output_tokens
                if max_output_tokens is None
                else max_output_tokens
            ),
        ),
    )
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text.strip()
