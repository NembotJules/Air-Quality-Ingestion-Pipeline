# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose port (optional, if you need to access the app externally)
# EXPOSE 8080

# Set environment variables (optional, if required)
# ENV VAR_NAME=value

# Command to run the ETL pipeline
CMD ["python", "pipelines/data_ingestion.py"]
