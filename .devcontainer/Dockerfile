# Use the official Python 3.10 image as a parent image
FROM python:3.10-slim-buster

# Set environment variables for non-interactive apt installs
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory in the container to /app
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome for Selenium
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb

# Copy only requirements to cache them in docker layer
COPY pyproject.toml .

# Copy all project files into the container
COPY immoweb_scraper .

# Copy the scripts directory into the container
COPY scripts /app/scripts

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false  && \ 
    poetry install

# Download chromedriver driver
RUN python /app/scripts/download_chromedriver.py 117.0.5938.88

# Command to run on container start
CMD ["poetry", "run", "scrape-immoweb"]