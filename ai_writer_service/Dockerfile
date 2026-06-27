# ── Stage 1: Build ────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build

# Install shared package first (for layer caching)
COPY shared/ /build/shared/
RUN pip install --no-cache-dir -e /build/shared/

# Install service dependencies
COPY ai-writer-service/requirements.txt /build/requirements.txt
RUN pip install --no-cache-dir -r /build/requirements.txt

# ── Stage 2: Runtime ──────────────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy shared library
COPY shared/ /app/shared/

# Copy service code
COPY ai-writer-service/app/ /app/app/

# Set Python path to include the shared library
ENV PYTHONPATH="/app:${PYTHONPATH}"
ENV PYTHONUNBUFFERED=1

EXPOSE 8002

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002", "--workers", "1"]
