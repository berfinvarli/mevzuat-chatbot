FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc g++ wget gnupg git curl \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/saidsurucu/mevzuat-mcp.git .

RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install chromium --with-deps

RUN pip install --no-cache-dir -e .

EXPOSE 8000

ENV PORT=8000
ENV PYTHONUNBUFFERED=1
ENV CONTAINER_ENV=1

HEALTHCHECK --interval=30s --timeout=10s --start-period=90s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
