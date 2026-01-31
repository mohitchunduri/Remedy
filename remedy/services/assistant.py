from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from google import genai
from google.genai import types


SYSTEM_PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts" / "system.md"


@dataclass
class GeminiConfig:
    api_key: str | None
    model: str
    temperature: float
    max_output_tokens: int

    @classmethod
    def from_env(cls) -> "GeminiConfig":
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
        temperature = float(os.environ.get("GEMINI_TEMPERATURE", "0.4"))
        max_output_tokens = int(os.environ.get("GEMINI_MAX_OUTPUT_TOKENS", "600"))
        return cls(
            api_key=api_key,
            model=model,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        )

    def is_configured(self) -> bool:
        return bool(self.api_key)


class Assistant:
    def __init__(self, config: GeminiConfig | None = None) -> None:
        self.config = config or GeminiConfig.from_env()
        self._client = genai.Client(api_key=self.config.api_key) if self.config.api_key else None

    def respond(self, message: str, history: list[dict[str, Any]] | None = None) -> dict:
        if not message:
            return {"status": "empty"}

        normalized = message.strip().lower()
        if normalized == "completed":
            return {
                "status": "completed",
                "reply": "Thanks for checking in. I have cleared this session. If you need anything later, just say hi.",
                "suggestions": ["Start a new check-in"],
            }

        if not self.config.is_configured():
            return {"status": "not-configured"}

        system_prompt = self._load_system_prompt()
        contents = list(history or []) + [{"role": "user", "parts": [{"text": message}]}]

        try:
            response = self._client.models.generate_content(
                model=self.config.model,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=self.config.temperature,
                    max_output_tokens=self.config.max_output_tokens,
                ),
            )
        except Exception:
            return {"status": "error"}

        text = (response.text or "").strip()
        payload = self._parse_json(text)
        normalized = self._normalize_payload(payload)
        if normalized:
            return normalized

        return {"reply": text} if text else {"status": "error"}

    def _load_system_prompt(self) -> str:
        return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")

    def _parse_json(self, text: str) -> dict | None:
        if not text:
            return None

        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            cleaned = cleaned.replace("json", "", 1).strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(cleaned[start : end + 1])
            except json.JSONDecodeError:
                return None
        return None

    def _normalize_payload(self, payload: dict | None) -> dict | None:
        if not isinstance(payload, dict):
            return None

        reply = payload.get("reply")
        if not isinstance(reply, str) or not reply.strip():
            return None

        normalized: dict[str, Any] = {"reply": reply.strip()}
        suggestions = payload.get("suggestions")
        if isinstance(suggestions, list):
            normalized["suggestions"] = [str(item) for item in suggestions][:3]
        return normalized
