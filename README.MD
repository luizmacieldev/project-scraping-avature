# 📄 Avature Job Scraper

## Project Overview

This project is a **web scraper for Avature-based career sites**. Its purpose is to automatically extract job postings, including detailed information about each position, from multiple companies using the Avature ATS (Applicant Tracking System).  

The scraper is designed to handle **HTML job listings**, providing a complete dataset for analysis or integration into other systems.

---

## Features

- **Generic scraping of Avature career sites** – Supports multiple companies by reading URLs from a configuration file.
- **Job metadata extraction** – Collects title, URL, job ID, source site, work location, business area, duration, and more.
- **HTML enrichment** – Extracts additional details and full job description from each job page.
- **Pagination handling** – Automatically navigates through multiple pages of job listings.
- **Custom headers and cookies** – Mimics a real browser to reduce the risk of being blocked.
- **Configurable fields** – Uses helper functions to normalize field names and allow generic scraping.

---

## Technologies

- **Python 3.9**
- **Scrapy** – Main web crawling framework.
- **Regular expressions** – For job ID extraction from URLs.
- **Custom headers** – To simulate real user behavior.

---

## How It Works

1. **Start Requests**  
    The spider starts from each site URL listed in the yaml file and requests the main job listing page.

2. **Listing Parsing**  
    The scraper extracts all job links from the listing pages and follows pagination links automatically.

3. **Job Parsing**  
    For each job URL:
    - Extracts the **job ID** from the URL.
    - Extracts fields from the HTML using **generic selectors**.
    - Extracts the **job description** by combining multiple content blocks.

4. **Item Creation**  
    After extraction, all data is merged into a single `AvatureJobItem` object and yielded for storage (JSON, CSV, or database).

---

## Project Structure

```
hiring_cafe_scrapy/
├── spiders/
│   ├── avature_spider.py       # Main spider for scraping Avature sites
│   └── __init__.py             # Spider package initialization
├── items.py                    # Defines the AvatureJobItem structure
├── pipelines.py                # Handles data processing and storage
├── settings.py                 # Scrapy project settings
├── middlewares.py              # Custom middlewares for request handling
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── scrapy.cfg                  # Scrapy configuration file
```

---

## Getting Started

### Prerequisites

- Python 3.9
- Pipenv or virtualenv for dependency management

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/luizmacieldev/test-scraping-avature.git
    cd test-scraping-avature
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Configure the scraper:
    - Add target URLs to a configuration file (e.g., `hiring_cafe/config/avature_sites.yaml`).

4. Run the scraper to save in JSON:
    ```bash
    cd hiring_cafe/hiring_cafe/
    scrapy crawl avature_spider -O avature_jobs.json
    ```

---

### Engineering Logic
One of the very first steps I took in this project was to identify and compile a list of companies that utilize the Avature ATS platform for their careers pages, such as `avature.net/careers`. I spent considerable time exploring the web, inspecting multiple company websites, and verifying which ones were built on this platform. This step was crucial to ensure that the scraping process would target relevant, consistent, and accessible sources, providing a solid foundation for collecting job postings in a structured and reliable way.


Then, I took was to carefully inspect each target site’s `robots.txt` file to ensure that scraping was permitted and to identify the allowed paths. <br />
I then thoroughly explored the browser’s developer console, inspecting all paginations, network requests, and potential API endpoints, but despite an extensive search, none of the sites provided public endpoints for job data.

As a result, I designed a generic HTML-based scraper capable of extracting job listings, details, and descriptions directly from the page content, using flexible selectors to handle variations between sites. During development, I encountered a `406 Not Acceptable` error from Nginx, which required configuring custom HTTP headers to mimic a real browser and avoid blocking. Additionally, to ensure data integrity, I implemented a pipeline that deduplicates job entries based on their `job_id`, guaranteeing that only unique jobs are included in the final dataset.

### Other Informations

The configuration file containing the list of sites to be scraped is located at:  
`hiring_cafe_scrapy/hiring_cafe/hiring_cafe/config/avature_sites.yaml`

The scraping results will be saved in:  
`hiring_cafe_scrapy/hiring_cafe/jobs.json`

- **Number of Avature ATS Sites Scraped:** 9  
- **Total Job Listings Collected:** 2,151

### Example of Data Extracted
The JSON below shows a single job posting extracted by the scraper. Each entry contains structured information about the job, including its title, location, business area, and a direct link to apply.

Example:

```json
{
  "title": "Senior Interaction Designer – Bloomberg Connects",
  "url": "https://bloomberg.avature.net/careers/JobDetail/Senior-Interaction-Designer-Bloomberg-Connects/15242",
  "source": "bloomberg",
  "job_id": "15242",
  "extracted_at": "2026-02-04T16:43:23.495508+00:00",
  "work_location": "New York",
  "business_area": "Engineering and CTO",
  "job_description": "Senior Interaction Designer – Bloomberg Connects\nDiscover what makes Bloomberg unique - watch our\nfor an inside look at our culture, values, and the people behind our success."
}





