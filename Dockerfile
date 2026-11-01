FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
# Apply available Debian security and package updates
RUN apt-get update \
    && apt-get upgrade -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt \
    && python -m pip uninstall -y pip

RUN useradd --create-home --uid 10001 appuser

COPY --chown=appuser:appuser scripts/ ./scripts/

USER appuser

CMD ["python", "-m", "scripts.generate_synthetic_data"]