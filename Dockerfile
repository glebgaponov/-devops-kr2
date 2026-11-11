FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN useradd --create-home --uid 10001 appuser

COPY --chown=appuser:appuser app.py .

USER appuser

EXPOSE 8003

CMD ["gunicorn", "--bind", "0.0.0.0:8003", "--workers", "2", "--timeout", "30", "app:app"]
