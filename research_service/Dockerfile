FROM python:3.11-slim

WORKDIR /app/research_service

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app:/app/research_service

COPY research_service/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY shared/ /app/shared/
COPY research_service/ /app/research_service/

EXPOSE 8004

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8004", "--workers", "1"]
