"""
AI Columnist Service — FastAPI Application.

This is the entry point for the AI Columnist microservice.
It creates the FastAPI app, registers routes, configures CORS,
and sets up structured error handling.

The service generates opinion-based analysis articles using the
research data produced by the Research Service. Unlike the
AI Writer (which creates factual news), this service produces
opinionated columns with pros/cons and recommendations.

Run locally:
    uvicorn app.main:app --host 0.0.0.0 --port 8005 --reload
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from shared.config import get_settings
from shared.exceptions import ServiceError, LLMProviderError
from shared.logging import setup_logging

from app.routes.columnist import router as columnist_router

# ── Settings & Logging ────────────────────────────────────────────────────
# get_settings() returns a singleton — safe to call multiple times.
# setup_logging() configures a structured logger for this service.

settings = get_settings()
logger = setup_logging("ai_columnist_service", level=settings.LOG_LEVEL)


# ── Lifespan ──────────────────────────────────────────────────────────────
# The lifespan context manager runs code on startup and shutdown.
# This is the modern FastAPI replacement for @app.on_event("startup").

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan: startup and shutdown logic."""
    logger.info(
        "AI Columnist Service starting | env=%s | llm_provider=%s",
        settings.ENVIRONMENT,
        settings.LLM_PROVIDER,
    )
    # --- Startup complete, hand control to the application ---
    yield
    # --- Shutdown begins ---
    logger.info("AI Columnist Service shutting down")


# ── FastAPI App ───────────────────────────────────────────────────────────
# The FastAPI instance with OpenAPI documentation enabled.

app = FastAPI(
    title="AI Newsroom — AI Columnist Service",
    description=(
        "AI Columnist service for the AI Newsroom Platform. "
        "Receives topic and research data, then generates a complete "
        "opinion article package with headline, opinion body, "
        "future trends, pros/cons, and recommendations."
    ),
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",          # Swagger UI at /docs
    redoc_url="/redoc",        # ReDoc at /redoc
    openapi_url="/openapi.json",
)


# ── CORS Middleware ───────────────────────────────────────────────────────
# Allow all origins for development. In production, restrict this
# to your frontend domain(s).

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # TODO: restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Routes ────────────────────────────────────────────────────────────────
# Include the columnist router. The router already has a /columnist prefix,
# so the full endpoints become:
#   POST /columnist/generate
#   GET  /columnist/health

app.include_router(columnist_router, tags=["Columnist"])


# ── Exception Handlers ───────────────────────────────────────────────────
# These handlers catch known exception types and return clean JSON errors
# instead of raw stack traces. Order matters: most specific first.

@app.exception_handler(LLMProviderError)
async def llm_provider_error_handler(
    request: Request, exc: LLMProviderError
) -> JSONResponse:
    """Handle LLM provider errors (connection failures, bad responses)."""
    logger.error("LLM Provider Error: %s", exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "llm_provider_error",
            "message": exc.message,
            "provider": exc.provider,
        },
    )


@app.exception_handler(ServiceError)
async def service_error_handler(
    request: Request, exc: ServiceError
) -> JSONResponse:
    """Handle general service errors (validation, repository, etc.)."""
    logger.error("Service Error: %s", exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "service_error",
            "message": exc.message,
        },
    )


@app.exception_handler(Exception)
async def general_error_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Catch-all for any unhandled exceptions — returns a safe 500 response."""
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "An unexpected error occurred",
        },
    )
