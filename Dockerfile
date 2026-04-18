FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    playwright \
    beautifulsoup4 \
    requests \
    lxml \
    tenacity

RUN playwright install chromium
RUN playwright install-deps

COPY parser_api.py .

EXPOSE 8000

CMD ["uvicorn", "parser_api:app", "--host", "0.0.0.0", "--port", "8000"]
