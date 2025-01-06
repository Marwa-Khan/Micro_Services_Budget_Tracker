# Stage 1: Build the frontend
FROM node:18 AS frontend-build

# Set working directory for the frontend
WORKDIR /simple-savings-sculptor

# Copy the frontend code
# COPY ../../simple-savings-sculptor/package.json ../../simple-savings-sculptor/package-lock.json ./
COPY simple-savings-sculptor/package.json simple-savings-sculptor/package-lock.json /simple-savings-sculptor/

RUN npm install

# Copy all frontendfiles
# COPY ../../simple-savings-sculptor ./  
COPY simple-savings-sculptor /simple-savings-sculptor/
RUN npm run build

# Stage 2: Setup the backend and integrate the frontend build
FROM python:3.9-slim AS backend-service

# Set the working directory for the backend
WORKDIR /app

# Copy all backend files (specific to auth_service)
COPY backend/auth_service /app/auth_service


# Install PostgreSQL client and development libraries
RUN apt-get update && apt-get install -y libpq-dev gcc && apt-get clean


# Copy the requirements file into the container
COPY backend/requirements.txt /app/requirements.txt


# Install shared Python requirements
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the built frontend into the backend static files directory
COPY --from=frontend-build /simple-savings-sculptor/dist ./static


# Expose the backend port
# EXPOSE 8000
EXPOSE 8001

# Command to run the backend
# CMD ["python", "auth_service/main.py"]

# CMD ["uvicorn", "main:auth_service", "--host", "0.0.0.0", "--port", "8001"]
CMD ["uvicorn", "auth_service.main:auth_service", "--host", "0.0.0.0", "--port", "8001"]

