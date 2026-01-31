from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class AIConfig:
    provider: str | None
    api_key: str | None
    model: str | None

    @classmethod
    def from_env(cls) -> "AIConfig":
        return cls(
            provider=os.environ.get("AI_PROVIDER"),
            api_key=os.environ.get("AI_API_KEY"),
            model=os.environ.get("AI_MODEL"),
        )

    def is_configured(self) -> bool:
        return bool(self.provider and self.api_key)


class Assistant:
    def __init__(self, config: AIConfig | None = None) -> None:
        self.config = config or AIConfig.from_env()

    def respond(self, message: str) -> dict:
        if not message:
            return {"status": "empty"}

        if not self.config.is_configured():
            return {"status": "not-configured"}

        return {"status": "not-implemented"}
