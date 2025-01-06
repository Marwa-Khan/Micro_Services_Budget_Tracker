# Stage 1: Build the frontend
FROM node:18 AS frontend-build

# Set working directory for the frontend
WORKDIR /simple-savings-sculptor

# Copy the frontend code
COPY simple-savings-sculptor/package.json simple-savings-sculptor/package-lock.json /simple-savings-sculptor/

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

# Copy backend-specific files
COPY backend/account_service /app/account_service
COPY backend/requirements.txt /app/

# Install the backend dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the built frontend into the backend static files directory
COPY --from=frontend-build /simple-savings-sculptor/dist /app/static

# Expose the backend port
# EXPOSE 8000
EXPOSE 8003


# Command to run the backend
# CMD ["python", "account_service/main.py"]
CMD ["uvicorn", "account_service.main:account_service", "--host", "0.0.0.0", "--port", "8003"]


