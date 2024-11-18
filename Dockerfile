# Use Python 3.9.6 as the base image
FROM python:3.9.6-slim

# Install system dependencies for Ollama and Python
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    libssl-dev \
    libcurl4-openssl-dev

# Install Ollama CLI
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set the working directory
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire content of the current directory into the /app folder in the container
COPY . .

# Expose the necessary ports: 8000 for your API and 11434 for Ollama service
EXPOSE 8000 11434

# Start Gunicorn and Ollama server, and pull the Llama3 model at runtime
CMD ["sh", "-c", "ollama serve & sleep 10 && ollama pull llama3 && uvicorn mindinventory_app:app --host 0.0.0.0 --port 8000"]
