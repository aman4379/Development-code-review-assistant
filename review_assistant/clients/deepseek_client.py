import os
from typing import Optional, Dict, Any

try:
    # OpenAI-compatible clients; deepseek provides an OpenAI API-compatible endpoint
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None  # type: ignore


class DeepSeekClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "deepseek-chat",
        temperature: float = 0.2,
        max_tokens: int = 2048,
    ) -> None:
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY") or ""
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

        self._client = None
        if self.api_key and OpenAI is not None:
            # DeepSeek uses OpenAI-compatible client; base_url may be needed depending on environment
            base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
            self._client = OpenAI(api_key=self.api_key, base_url=base_url)

    @property
    def is_available(self) -> bool:
        return self._client is not None

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        if not self._client:
            # Offline mode, no API available
            return self._offline_response(user_prompt)

        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            content = response.choices[0].message.content  # type: ignore[attr-defined]
            return content or ""
        except Exception as e:  # pragma: no cover
            return f"[LLM error] {e}"

    def _offline_response(self, user_prompt: str) -> str:
        # Extremely simple heuristic fallback
        hints = []
        lower = user_prompt.lower()
        if "print(" in lower or "console.log" in lower:
            hints.append("Use structured logging instead of print/console.log in production.")
        if "except:" in lower:
            hints.append("Avoid bare except; catch specific exceptions.")
        if "eval(" in lower:
            hints.append("Avoid eval due to security risks; prefer safe parsers.")
        if "todo" in lower:
            hints.append("Resolve TODOs before merging to main.")
        if not hints:
            hints.append("Ensure readability, small functions, and clear naming.")
        return "\n- ".join(["Offline heuristic suggestions:"] + hints)
