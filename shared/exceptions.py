"""
Custom exception hierarchy for the AI Newsroom Platform.

All services use these exceptions for consistent error handling
and HTTP error response mapping.
"""


class ServiceError(Exception):
    """Base exception for all service-level errors."""

    def __init__(self, message: str = "An internal service error occurred", status_code: int = 500) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class LLMProviderError(ServiceError):
    """Base exception for LLM provider errors."""

    def __init__(self, message: str = "LLM provider error", provider: str = "unknown") -> None:
        self.provider = provider
        super().__init__(message=f"[{provider}] {message}", status_code=502)


class LLMConnectionError(LLMProviderError):
    """Raised when unable to connect to the LLM provider."""

    def __init__(self, provider: str, detail: str = "") -> None:
        msg = f"Connection failed to LLM provider"
        if detail:
            msg += f": {detail}"
        super().__init__(message=msg, provider=provider)


class LLMResponseError(LLMProviderError):
    """Raised when the LLM provider returns an invalid or empty response."""

    def __init__(self, provider: str, detail: str = "") -> None:
        msg = f"Invalid response from LLM provider"
        if detail:
            msg += f": {detail}"
        super().__init__(message=msg, provider=provider)


class ValidationError(ServiceError):
    """Raised when input validation fails beyond Pydantic checks."""

    def __init__(self, message: str = "Validation error") -> None:
        super().__init__(message=message, status_code=422)


class RepositoryError(ServiceError):
    """Raised for future database/repository layer errors."""

    def __init__(self, message: str = "Repository error") -> None:
        super().__init__(message=message, status_code=500)
