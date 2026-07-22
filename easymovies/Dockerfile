# Base Image
FROM python:3.12-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure Python output is sent straight to terminal
ENV PYTHONUNBUFFERED=1

# Create working directory
WORKDIR /app

# Install dependencies first (better Docker layer caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose Flask port
EXPOSE 8081

# Start application
CMD ["python", "app.py"]