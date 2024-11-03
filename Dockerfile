# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables to prevent Python from writing .pyc files and to buffer output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev libssl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y gcc python3-dev && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Copy the rest of the application code into the container
COPY . .

# Expose port 8000 for the Django app
EXPOSE 8000

# Run the application with HTTPS using runserver_plus
CMD ["bash", "-c", "if [ ! -f /app/certs/cert.pem ]; then mkdir -p /app/certs && openssl req -x509 -newkey rsa:4096 -nodes -out /app/certs/cert.pem -keyout /app/certs/key.pem -days 365 -subj '/CN=*'; fi && python manage.py runserver_plus 0.0.0.0:8000 --cert-file /app/certs/cert.pem --key-file /app/certs/key.pem"]
