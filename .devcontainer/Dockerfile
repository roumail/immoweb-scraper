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

# Install specific version of Chrome for Selenium
RUN wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/117.0.5938.88/linux64/chrome-linux64.zip \
    && unzip chrome-linux64.zip -d /usr/bin \
    && rm chrome-linux64.zip

# Copy only requirements to cache them in docker layer
COPY pyproject.toml README.md ./

# Copy all project files into the container
COPY ./immoweb_scraper/ ./immoweb_scraper/

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false  && \ 
    poetry install

# Download chromedriver driver
RUN ["poetry", "run", "download-chromedriver", "117.0.5938.88"]

# Command to run on container start
CMD ["poetry", "run", "scrape-immoweb"]