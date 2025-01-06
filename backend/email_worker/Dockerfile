# Use the official Python image as a base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app


# Copy only the necessary files for the worker_email service
COPY backend/email_worker /app/email_worker

# Install the necessary dependencies
# RUN pip install --upgrade pip
COPY backend/email_worker/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Expose port if needed for the application, RabbitMQ default port
EXPOSE 5672


# Command to run the email_worker service when the container starts
CMD ["python", "email_worker/main.py"]
