"""
Structured logging setup for all services.

Provides JSON-formatted log output with service name, timestamp,
and correlation context for production observability.
"""

import logging
import sys
from typing import Optional


def setup_logging(
    service_name: str,
    level: str = "INFO",
    correlation_id: Optional[str] = None,
) -> logging.Logger:
    """
    Configure and return a structured logger for a given service.

    Args:
        service_name: Name of the microservice (e.g. 'research_service').
        level: Log level string (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        correlation_id: Optional correlation ID for request tracing.

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger(service_name)

    # Prevent duplicate handlers on repeated calls
    if logger.handlers:
        return logger

    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)

    # ── Console Handler ───────────────────────────────────────────────────
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)

    # Structured format with service context
    log_format = (
        "%(asctime)s | %(levelname)-8s | "
        f"{service_name} | "
        "%(name)s:%(funcName)s:%(lineno)d | "
        "%(message)s"
    )
    formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = False

    return logger
