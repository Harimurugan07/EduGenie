import json
from typing import Any, TypeVar

from google import genai
from google.genai import types
from pydantic import BaseModel

from config import settings

T = TypeVar("T", bound=BaseModel)


class GeminiConfigurationError(RuntimeError):
    pass


class GeminiGenerationError(RuntimeError):
    pass


class GeminiClient:
    def __init__(self) -> None:
        if not settings.gemini_api_key:
            raise GeminiConfigurationError(
                "GEMINI_API_KEY is not configured. Add it to your .env file."
            )
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = settings.gemini_model

    def text(self, prompt: str, *, temperature: float = 0.3) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=2048,
                ),
            )
            text = getattr(response, "text", None)
            if not text:
                raise GeminiGenerationError("Gemini returned an empty response.")
            return text.strip()
        except GeminiGenerationError:
            raise
        except Exception as exc:
            raise GeminiGenerationError(f"Gemini request failed: {exc}") from exc

    def structured(
        self,
        prompt: str,
        schema: type[T],
        *,
        temperature: float = 0.2,
    ) -> T:
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=4096,
                    response_mime_type="application/json",
                    response_schema=schema,
                ),
            )

            parsed = getattr(response, "parsed", None)
            if parsed is not None:
                if isinstance(parsed, schema):
                    return parsed
                return schema.model_validate(parsed)

            raw = getattr(response, "text", None)
            if not raw:
                raise GeminiGenerationError("Gemini returned no structured output.")

            return schema.model_validate(json.loads(raw))
        except GeminiGenerationError:
            raise
        except Exception as exc:
            raise GeminiGenerationError(
                f"Gemini structured generation failed: {exc}"
            ) from exc


_client: GeminiClient | None = None


def get_gemini_client() -> GeminiClient:
    global _client
    if _client is None:
        _client = GeminiClient()
    return _client
