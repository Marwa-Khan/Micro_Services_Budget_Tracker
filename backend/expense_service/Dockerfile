# Stage 1: Build the frontend
FROM node:18 AS frontend-build

# Set working directory for the frontend
WORKDIR /simple-savings-sculptor

# Copy the frontend code
COPY simple-savings-sculptor/package.json simple-savings-sculptor/package-lock.json /simple-savings-sculptor/

# Install frontend dependencies
RUN npm install

# Copy all frontend files
COPY simple-savings-sculptor /simple-savings-sculptor/
RUN npm run build

# Stage 2: Setup the backend and integrate the frontend build
FROM python:3.9-slim AS backend-service

# Set the working directory for the backend
WORKDIR /app

# Install PostgreSQL client and development libraries
RUN apt-get update && apt-get install -y libpq-dev gcc && apt-get clean


# Copy the backend files for the expense_service
COPY backend/expense_service /app/expense_service



# Copy the requirements file
COPY backend/requirements.txt /app/requirements.txt


# Install RabbitMQ client dependencies
RUN pip install --no-cache-dir pika

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt


# Copy the built frontend into the backend static files directory
COPY --from=frontend-build /simple-savings-sculptor/dist /app/static


# Set environment variable for RabbitMQ
ENV RABBITMQ_HOST=localhost

# Expose the backend port
EXPOSE 8002

# Command to run the backend
# CMD ["python", "/app/expense_service/main.py"]
CMD ["uvicorn", "expense_service.main:expense_service", "--host", "0.0.0.0", "--port", "8002"]