FROM --platform=linux/amd64 python:3.10

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    PyPDF2==3.0.1 \
    PyMuPDF==1.23.8

# Copy the processing script
COPY src/process_pdfs.py .

# Run the script
CMD ["python", "process_pdfs.py"] 