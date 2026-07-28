"""
Centralized configuration using python-dotenv + os.getenv.

Loads the .env file from the project root on import, then reads
all environment variables with simple os.getenv() calls.
Future database URLs (PostgreSQL, Redis, Qdrant) are included as placeholders.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ── Load .env from project root ──────────────────────────────────────────
# shared/config.py -> shared/ -> AI_News/ (project root)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_ENV_FILE = _PROJECT_ROOT / ".env"

load_dotenv(_ENV_FILE, override=True)


# ── Settings Class ───────────────────────────────────────────────────────

class Settings:
    """Application-wide settings loaded from environment variables."""

    def __init__(self):
        # ── General ───────────────────────────────────────────────────
        self.ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
        self.DEBUG: bool = os.getenv("DEBUG", "true").lower() in ("true", "1", "yes")

        # ── LLM Provider Selection ────────────────────────────────────
        self.LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "ollama")

        # ── Ollama ────────────────────────────────────────────────────
        self.OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3")

        # ── Groq ──────────────────────────────────────────────────────
        self.GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
        self.GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

        # ── Gemini ────────────────────────────────────────────────────
        self.GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
        self.GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

        # ── NVIDIA NIM ────────────────────────────────────────────────
        self.NVIDIA_API_KEY: str = os.getenv("NVIDIA_API_KEY", "")
        self.NVIDIA_BASE_URL: str = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
        self.NVIDIA_MODEL: str = os.getenv("NVIDIA_MODEL", "meta/llama-3.1-8b-instruct")

        # ── Future: Database Connections (placeholders) ───────────────
        self.DATABASE_URL: str = os.getenv("DATABASE_URL", "")
        self.REDIS_URL: str = os.getenv("REDIS_URL", "")
        self.QDRANT_URL: str = os.getenv("QDRANT_URL", "")


# ── Singleton ────────────────────────────────────────────────────────────
_settings_instance = None


def get_settings() -> Settings:
    """Returns a cached Settings instance (singleton)."""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance
