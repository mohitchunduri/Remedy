from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SessionState:
    history: list[dict[str, Any]] = field(default_factory=list)
    max_messages: int = 12

    @classmethod
    def load(cls, flask_session) -> "SessionState":
        history = flask_session.get("history", [])
        return cls(history=history)

    def add_user(self, text: str) -> None:
        self.history.append({"role": "user", "parts": [{"text": text}]})
        self._trim()

    def add_model(self, text: str) -> None:
        self.history.append({"role": "model", "parts": [{"text": text}]})
        self._trim()

    def save(self, flask_session) -> None:
        flask_session["history"] = self.history

    def clear(self, flask_session) -> None:
        flask_session.pop("history", None)
        self.history = []

    def _trim(self) -> None:
        if len(self.history) > self.max_messages:
            self.history = self.history[-self.max_messages :]
