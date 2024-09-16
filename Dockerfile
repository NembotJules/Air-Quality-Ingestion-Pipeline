# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports for Prefect server and UI
EXPOSE 8080 4200

# Start the Prefect server
CMD ["prefect", "server", "start"]