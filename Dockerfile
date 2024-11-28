# Use the official Python image as the base image
FROM python:3.9-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1  # Prevents writing .pyc files
ENV PYTHONUNBUFFERED 1         # Ensures logs are output in real-time

# Set the working directory inside the container
WORKDIR /app

# Copy the application code to the container
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the Flask port
EXPOSE 5000

# Command to start the application
CMD ["python", "run.py"]