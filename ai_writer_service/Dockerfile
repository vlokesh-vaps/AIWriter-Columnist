FROM python:3.11-slim

WORKDIR /app/ai_writer_service

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app:/app/ai_writer_service

COPY ai_writer_service/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY shared/ /app/shared/
COPY ai_writer_service/ /app/ai_writer_service/

EXPOSE 8002

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002", "--workers", "1"]
