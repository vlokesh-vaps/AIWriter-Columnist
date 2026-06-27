"""Service-specific configuration for the Fact-Check Service."""

from shared.config import Settings, get_settings

SERVICE_NAME = "fact_check_service"
SERVICE_VERSION = "0.1.0"

__all__ = ["Settings", "get_settings", "SERVICE_NAME", "SERVICE_VERSION"]
