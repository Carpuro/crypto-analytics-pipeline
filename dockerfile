FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY src/ ./src/
COPY sql/ ./sql/

# Create data directory
RUN mkdir -p data

# Run the ingestion script
CMD ["python", "src/ingest_crypto_data.py"]