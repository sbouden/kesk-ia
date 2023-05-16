# Base image
FROM python:3.9-slim-buster

# Install dependencies
COPY requirements.txt /app/
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . /app

# Set environment variables
ENV PORT=8080

# Start the app
CMD ["python", "app.py"]
