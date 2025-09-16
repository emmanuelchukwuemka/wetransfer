# Use official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Expose port (Render will provide PORT env variable)
EXPOSE $PORT

# Set environment variables for Flask
ENV FLASK_APP=index.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask app with Gunicorn for production
CMD gunicorn --bind 0.0.0.0:$PORT index:app
