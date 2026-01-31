from __future__ import annotations

from flask import Blueprint, jsonify, render_template, request, session

from .services.assistant import Assistant
from .services.session_state import SessionState

bp = Blueprint("main", __name__)


@bp.route("/")
def index() -> str:
    return render_template("index.html")


@bp.route("/chat", methods=["POST"])
def chat():
    payload = request.get_json(silent=True) or {}
    message = (payload.get("message") or "").strip()

    assistant = Assistant()
    state = SessionState.load(session)
    response = assistant.respond(message, state.history)

    if response.get("status") == "completed":
        state.clear(session)
        return jsonify(response)

    reply = response.get("reply")
    if reply:
        state.add_user(message)
        state.add_model(reply)
        state.save(session)
    return jsonify(response)
