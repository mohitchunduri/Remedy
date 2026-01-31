from __future__ import annotations

import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-remedy-ui")
    TEMPLATES_AUTO_RELOAD = True
