# Use official lightweight Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code
COPY . .

# Set environment variable for Python output buffering
ENV PYTHONUNBUFFERED=1

# Command to run your bot
CMD ["python", "main.py"]