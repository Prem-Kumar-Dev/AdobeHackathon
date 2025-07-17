# Adobe India Hackathon 2025 - Unified Solution (Optimized)
# Supports both Round 1A and Round 1B automatically
FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

# Install system dependencies and Python packages in one layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    && pip install --no-cache-dir \
        PyPDF2==3.0.1 \
        PyMuPDF==1.26.3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /root/.cache/pip

# Copy the entire source code
COPY src/ ./src/
COPY main.py .

# Create input, output, and persona directories
RUN mkdir -p /app/input /app/output /app/persona

# Run the unified solution
CMD ["python", "main.py"] 