# syntax=docker/dockerfile:1
# Pull official python base image
FROM python:3

# Prevent python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Prevent python from buffering stdin/stdout
ENV PYTHONUNBUFFERED=1

# Create and set working directory in container
WORKDIR /scheduler_service

# Copy and install requirements 
COPY requirements.txt /scheduler_service/
RUN pip install -r requirements.txt
COPY . /scheduler_service/
