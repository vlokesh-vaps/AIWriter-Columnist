FROM python:3.11-slim

WORKDIR /app/ai_columnist_service

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app:/app/ai_columnist_service

COPY ai_columnist_service/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY shared/ /app/shared/
COPY ai_columnist_service/ /app/ai_columnist_service/

EXPOSE 8005

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8005", "--workers", "1"]
