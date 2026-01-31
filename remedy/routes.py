from __future__ import annotations

from flask import Blueprint, jsonify, render_template, request

from .services.assistant import Assistant

bp = Blueprint("main", __name__)


@bp.route("/")
def index() -> str:
    return render_template("index.html")


@bp.route("/chat", methods=["POST"])
def chat():
    payload = request.get_json(silent=True) or {}
    message = (payload.get("message") or "").strip()

    assistant = Assistant()
    response = assistant.respond(message)
    return jsonify(response)
