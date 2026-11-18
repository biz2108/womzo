
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./

RUN python -m pip install --no-cache-dir --upgrade pip==26.3 \
    && python -m pip install --no-cache-dir -r requirements.txt

COPY app.py VERSION ./
COPY templates ./templates
COPY static ./static

EXPOSE 8000

CMD ["gunicorn", "--no-control-socket", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "2", "--timeout", "30", "app:app"]
