# Adobe India Hackathon 2025 - Unified Solution
# Supports both Round 1A and Round 1B automatically
FROM --platform=linux/amd64 python:3.10

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    PyPDF2==3.0.1 \
    PyMuPDF==1.26.3

# Copy the entire source code
COPY src/ ./src/
COPY main.py .

# Create input, output, and persona directories
RUN mkdir -p /app/input /app/output /app/persona

# Run the unified solution
CMD ["python", "main.py"] 