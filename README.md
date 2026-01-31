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

## Gemini config
- `GEMINI_API_KEY` your Gemini API key (or `GOOGLE_API_KEY`)
- `GEMINI_MODEL` model id (default: `gemini-2.5-flash`)
- `GEMINI_TEMPERATURE` optional (default: `0.4`)
- `GEMINI_MAX_OUTPUT_TOKENS` optional (default: `600`)

Example:
```bash
export GEMINI_API_KEY=YOUR_KEY_HERE
export GEMINI_MODEL=gemini-2.5-flash
```
