import os
from functools import lru_cache
from typing import List, Optional

# Optional: .env automatisch laden (praktisch für lokale Entwicklung)
# In Produktion machst du das über Docker / Hosting-Env.
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    # python-dotenv ist im requirements.txt, aber falls nicht installiert,
    # crasht hier nichts.
    pass


class Settings:
    """Central configuration for the CollectiVAI Router.

    Values are loaded from environment variables.
    In production, configure these via your hosting platform (Cloudflare, Docker, etc.).
    """

    # --- Core / Router ---
    env: str               # e.g. "development", "production"
    log_level: str         # e.g. "info", "debug"
    default_timeout: int   # seconds for provider HTTP calls

    # CORS
    allowed_origins: List[str]

    # Provider API keys
    openai_api_key: Optional[str]
    gemini_api_key: Optional[str]
    mistral_api_key: Optional[str]
    meta_api_key: Optional[str]
    deepseek_api_key: Optional[str]

    # Optional custom backend (for future extensions)
    custom_backend_url: Optional[str]
    custom_backend_token: Optional[str]

    def __init__(self) -> None:
        # --- Core / Router ---
        self.env = os.getenv("ROUTER_ENV", "development")
        self.log_level = os.getenv("ROUTER_LOG_LEVEL", "info")

        # Default timeout für HTTP-Calls zu den Providern (secs)
        timeout_str = os.getenv("ROUTER_DEFAULT_TIMEOUT", "60")
        try:
            self.default_timeout = int(timeout_str)
        except ValueError:
            self.default_timeout = 60

        # --- CORS ---
        origins = os.getenv("ROUTER_ALLOWED_ORIGINS", "")
        self.allowed_origins = [o.strip() for o in origins.split(",") if o.strip()]

        # --- Provider API keys ---
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.mistral_api_key = os.getenv("MISTRAL_API_KEY")
        self.meta_api_key = os.getenv("META_API_KEY")
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")

        # --- Optional custom backend ---
        self.custom_backend_url = os.getenv("CUSTOM_BACKEND_URL")
        self.custom_backend_token = os.getenv("CUSTOM_BACKEND_TOKEN")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a singleton Settings instance (FastAPI-friendly)."""
    return Settings()
