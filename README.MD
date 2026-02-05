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

- **Python 3.8**
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
hiring_cafe/
├── spiders/
│   ├── avature_spider.py        # Main spider for scraping Avature ATS sites
│   └── __init__.py              # Spider package initialization
│
├── common/
│   ├── __init__.py
│   └── functions.py             # Reusable helper and utility functions
│
├── config/
│   └── avature_sites.yaml       # List of Avature-hosted sites to be scraped
│
├── items.py                     # Defines the AvatureJobItem structure
├── pipelines.py                 # Item pipelines (deduplication, cleaning, output)
├── settings.py                  # Scrapy project settings
├── middlewares.py               # Custom downloader middlewares (e.g. User-Agent rotation)
│
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
└── scrapy.cfg                   # Scrapy configuration file

```

---

## Getting Started

### Prerequisites

- Python 3.8
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
    scrapy crawl avature_spider -O jobs.json
    ```

---

### Engineering Logic
One of the very first steps in this project was identifying and compiling a list of companies that use the Avature ATS platform for their careers pages (e.g., *.avature.net/careers). I spent significant time researching the web, inspecting multiple company career sites, and verifying which ones were built on Avature. This step was essential to ensure that the scraping process targeted relevant, consistent, and accessible sources, providing a solid foundation for collecting job postings in a structured and reliable manner.

Next, I carefully inspected each target site’s robots.txt file to confirm that scraping was permitted and to understand which paths were allowed. I then thoroughly explored each site using the browser’s developer tools, analyzing pagination behavior, network requests, and potential API endpoints. Despite an extensive investigation, none of the sites exposed public or reusable APIs for accessing job data.

As a result, I designed a generic HTML-based scraping solution using Scrapy, capable of extracting job listings, job details, and descriptions directly from the rendered page content. The scraper relies on flexible and resilient selectors to accommodate structural variations across different Avature-hosted sites.

During development, I encountered 406 Not Acceptable responses from Nginx, which indicated server-side filtering of non-browser-like requests. To address this, I implemented a custom downloader middleware that rotates User-Agent headers periodically, mimicking real browser traffic and reducing the likelihood of request blocking. The middleware swaps the User-Agent every few requests, improving request acceptance and scraper stability.

In addition, to ensure data quality and integrity, I implemented a Scrapy item pipeline responsible for deduplicating job entries based on their job_id. This guarantees that each job appears only once in the final dataset, even when the same posting is encountered multiple times due to pagination or navigation paths.

Overall, this approach prioritizes robustness, compliance, and data cleanliness, while remaining adaptable to differences across Avature-powered career sites.

### Other Informations

The configuration file containing the list of sites to be scraped is located at:  
`test-scraping-avature/hiring_cafe/hiring_cafe/config/avature_sites.yaml`

The scraping results will be saved in:  
`test-scraping-avature/hiring_cafe/jobs.json`

- **Number of Avature ATS Sites Scraped:** 9  
- **Total Job Listings Collected:** 2,151

### Example of Data Extracted
The JSON below shows a single job posting extracted by the scraper. Each entry contains structured information about the job, including its title, location, business area, and a direct link to apply.

Example:

```json
{
  "title": "Senior Custodian, Per Diem - Ronald Reagan Medical Center",
  "url": "https://uclahealth.avature.net/careers/JobDetail/Senior-Custodian-Per-Diem-Ronald-Reagan-Medical-Center/28870",
  "source": "ucla_health",
  "job_id": "28870",
  "extracted_at": "2026-02-04T23:17:42.058013+00:00",
  "posted_date": "02/03/2026",
  "duration": "Indefinite",
  "job_description": "Work Location: Los Angeles, CA, USA Onsite or Remote Fully On-Site Work Schedule 7:00am - 3:30pm on variable days including weekends and holidays Posted Date 02/03/2026 Salary Range : $27.09 - 27.09 Hourly Employment Type 6 - Staff: Per Diem Duration Indefinite Job # 28784 This position may be converted to career . Serving at UCLA Health will give you the opportunity to use your specialized abilities to help improve the lives of our patients, their families, and your fellow UCLA Health team members. You'll provide critical support that makes healing happen. We'd love to have you join us. Under the supervision of a Custodial supervisor - Clean assigned areas, patient rooms, nursing station, ancillary rooms, exam rooms, procedure rooms, conference rooms, office's, hallways, corridor, public areas, etc. Operate vacuum cleaners, buffers, wall and window washing, shampoo machines and floor machine. Sweep, strip and wax floors. Perform isolation room cleaning. Perform high and low dusting. Clean vertical and horizontal surfaces using the approved cleaning solutions. They have knowledge in the correct use and storage of disinfectants, cleaning solution, soap, detergents and floor waxes preferred. Salary Rate: $27.09 / hourly Ability to exercise tact and diplomacy while directing co-workers. Ability to interact effectively with patients, customers and associates in a way that exhibits superior integrated customer service and teamwork. Ability to operate all types of housekeeping equipment (vacuum cleaners, floor machines, carpet extractors, auto scrubbers, pressure / steam cleaning machine etc). Ability to perform and prioritize multiple tasks effectively and efficiently. Ability to read, write, comprehend and communicate in English. Ability to take initiative and follow through. Ability to work within defined time constraints. Excellent listening and verbal communication skills. Excellent organization and problem solving skills. Must be able to frequently: Bend waist while standing. Lift, push and pull a minimum of 50 lbs. Stoop and squat. Twisting and bending of the neck forward and backward. Work in standing position for long periods."
}





