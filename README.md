# Remedy
Health support for free, when using Remedy.

## Local run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:5000`.

## Structure
- `app.py` entrypoint
- `remedy/__init__.py` app factory
- `remedy/routes.py` Flask routes and API endpoints
- `remedy/services/assistant.py` AI integration stub (wire provider + Supabase here)
- `remedy/templates/index.html` UI markup
- `remedy/static/` styles and chat UI logic

## AI config (stub)
- `AI_PROVIDER` name of provider (ex: openai, anthropic)
- `AI_API_KEY` API key for the provider
- `AI_MODEL` model identifier
