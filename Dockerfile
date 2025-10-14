FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create logs directory
RUN mkdir -p /app/logs

# Expose honeypot ports
EXPOSE 2121 2222 8080

# Run the honeypot
CMD ["python3", "main.py"]
