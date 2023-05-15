# Base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files to container
COPY . /app
RUN chmod +x /app/stream.sh

# Expose port
EXPOSE 8501

# Set entrypoint
ENTRYPOINT ["/bin/bash", "stream.sh"]