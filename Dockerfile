# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY ./app/requirements.txt /app/requirements.txt

# Install any dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the entire app directory into the container
COPY ./app /app

# Expose the port on which FastAPI will run
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]