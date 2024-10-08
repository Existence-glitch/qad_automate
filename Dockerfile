# Use Python 3.11 slim image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create logs directory and set permissions
RUN mkdir -p /app/logs && chmod 777 /app/logs

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME QADAutomate

# Run the scheduler when the container launches
CMD ["python", "src/scheduler.py"]