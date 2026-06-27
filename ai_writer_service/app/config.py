"""Service-specific configuration for the AI Writer Service."""

from shared.config import Settings, get_settings

SERVICE_NAME = "ai_writer_service"
SERVICE_VERSION = "0.1.0"

__all__ = ["Settings", "get_settings", "SERVICE_NAME", "SERVICE_VERSION"]
