# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . .

# Make port 9050 available to the world outside this container
EXPOSE 9050

# Define environment variable for Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Create logs directory
RUN mkdir -p logs

# Run main.py when the container launches
CMD ["python", "main.py"]