# immoweb-scraper
immoweb-scraper is a Python-based tool designed to scrape property listings from the Immoweb website. The idea is to use the scraped data as a way to experiment with modeling exercises and as a way to experiment with different scraping, data engineering workflows. The results of the scraping are added to an sqlite database. The dependencies for this project are managed via `poetry`.

## Future plans

* Scheduler to run the scraping tasks and accumulate data slowly over time. 
* Dockerize the analysis 
* Investigate decoupled architecture of microservices


## Usage
After installing the package using your favourite, you can run the package entrypoint `scrape-immoweb`.  
This script initializes the database, and starts the scraping process.


