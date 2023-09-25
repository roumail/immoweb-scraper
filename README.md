# immoweb-scraper
immoweb-scraper is a Python-based tool designed to scrape property listings from the Immoweb website. The idea is to use the scraped data as a way to experiment with modeling exercises and as a way to experiment with different scraping, data engineering workflows. This codebase uses Prefect to schedule regular scraping scraping tasks. The results of the scraping are added to an sqlite database. Eventually, we will add tasks to make modelling views of the collected data and make backups of the database.

## Architecture Overview

We use a python package to separate components for separating concerns into database connections, scraping logic, URL generation, and browser setup. The dependencies for this project are managed via `poetry`.


## Usage
After installing the package using your favourite, you can run the package entrypoint `scrape-immoweb`.  
This script sets up the browser, initializes the database, and starts the scraping process.


