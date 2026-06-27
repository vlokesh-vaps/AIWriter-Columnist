"""
Shared Pydantic schemas for the AI Newsroom Platform.
"""

from shared.schemas.research import ResearchRequest, ResearchResponse
from shared.schemas.writer import WriterRequest, WriterResponse
from shared.schemas.fact_check import FactCheckRequest, FactCheckResponse
from shared.schemas.columnist import ColumnistRequest, ColumnistResponse
from shared.schemas.health import HealthResponse

__all__ = [
    "ResearchRequest",
    "ResearchResponse",
    "WriterRequest",
    "WriterResponse",
    "FactCheckRequest",
    "FactCheckResponse",
    "ColumnistRequest",
    "ColumnistResponse",
    "HealthResponse",
]
