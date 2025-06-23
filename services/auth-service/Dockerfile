# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Create a non-root user and group
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Using --no-cache-dir to reduce image size
# Using --user to install packages as the non-root user (if possible and makes sense for the build step)
# However, for system-level dependencies often needed by psycopg2-binary, it's better to install them as root first.
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y --auto-remove gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy the rest of the application code into the container at /app
COPY . .

# Change ownership of the app directory to the non-root user
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable for the application port (optional, can be overridden)
ENV PORT 8000
ENV HOST 0.0.0.0

# Run main.py when the container launches
# Use uvicorn with host 0.0.0.0 to be accessible from outside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Healthcheck (optional but recommended)
# HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
#   CMD curl -f http://localhost:8000/ || exit 1
# Note: curl is not available in python:3.11-slim by default.
# If you need a healthcheck with curl, you might need to install it or use a different base image,
# or use a Python script for the healthcheck.
# For now, we'll rely on Docker's default healthcheck or Compose healthchecks.
