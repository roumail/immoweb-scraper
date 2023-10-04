# Use the official Python 3.10 image as a parent image
FROM python:3.10-slim-buster

# Set environment variables for non-interactive apt installs
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory in the container to /app
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    git \
    unzip \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements to cache them in docker layer
COPY pyproject.toml README.md ./

# Copy all project files into the container
COPY ./immoweb_scraper/ ./immoweb_scraper/

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false  && \ 
    poetry install

# Command to run on container start
CMD ["poetry", "run", "scrape-immoweb"]