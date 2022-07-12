# syntax=docker/dockerfile:1
# Pull official python base image
FROM python:3.10

# Prevent python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Prevent python from buffering stdin/stdout
ENV PYTHONUNBUFFERED=1

# Create and set working directory in container
WORKDIR /scheduler_service

# Copy and install requirements 
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./requirements-testpypi.txt .
RUN pip install -r requirements-testpypi.txt

# Copy entrypoint.sh
COPY ./entrypoint.sh /scheduler_service/entrypoint.sh
# Provide executable permissions to entrypoint script
RUN chmod +x /scheduler_service/entrypoint.sh

# Copy project
COPY . .

# Run entrypoint.sh to automatically apply migrations
# ENTRYPOINT ["sh", "/scheduler_service/entrypoint.sh"]