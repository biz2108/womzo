FROM python:3.12-slim

LABEL org.opencontainers.image.title="SJB's World Webcams" \
      org.opencontainers.image.description="A lightweight, self-hosted webcam viewer" \
      org.opencontainers.image.vendor="SJB Projects" \
      org.opencontainers.image.source="https://github.com/biz2108/sjb-world-webcams" \
      org.opencontainers.image.licenses="AGPL-3.0-only"

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./

RUN python -m pip install --no-cache-dir --upgrade pip==26.3 \
    && python -m pip install --no-cache-dir -r requirements.txt

COPY app.py VERSION LICENSE THIRD_PARTY_NOTICES.md ./
COPY templates ./templates
COPY static ./static

EXPOSE 8000

CMD ["gunicorn", "--no-control-socket", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "2", "--timeout", "30", "app:app"]
