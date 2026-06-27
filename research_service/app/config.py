"""Service-specific configuration for the Research Service."""

from shared.config import Settings, get_settings

# Service-specific settings can extend the base Settings class here
# For now, we reuse the shared Settings directly.

SERVICE_NAME = "research_service"
SERVICE_VERSION = "0.1.0"

__all__ = ["Settings", "get_settings", "SERVICE_NAME", "SERVICE_VERSION"]
