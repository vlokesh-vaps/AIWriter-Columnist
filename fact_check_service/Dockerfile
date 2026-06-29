FROM python:3.11-slim

WORKDIR /app/fact_check_service

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app:/app/fact_check_service

COPY fact_check_service/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY shared/ /app/shared/
COPY fact_check_service/ /app/fact_check_service/

EXPOSE 8003

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003", "--workers", "1"]
