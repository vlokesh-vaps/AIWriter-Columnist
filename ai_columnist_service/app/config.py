"""
Service-specific configuration for the AI Columnist Service.

Imports shared settings and defines service-level constants
(name, version) used by routes and logging.
"""

from shared.config import Settings, get_settings

# ── Service Identity ──────────────────────────────────────────────────────
# These constants appear in health checks, logs, and OpenAPI docs.

SERVICE_NAME = "ai_columnist_service"
SERVICE_VERSION = "0.1.0"

__all__ = ["Settings", "get_settings", "SERVICE_NAME", "SERVICE_VERSION"]
