
FROM python:3.12-slim

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


ENV PYTHONUNBUFFERED=1


CMD ["python", "main.py"]
