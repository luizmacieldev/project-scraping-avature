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
{"title": "Enrollment and Eligibility Subject Matter Expert", "url": "https://maximus.avature.net/careers/FolderDetail/United-States-Consulting-PMC-AL-E-E-SME-AK-BID-01-26/35182", "source": "maximus", "job_id": "01", "extracted_at": "2026-02-04T19:30:18.620459+00:00", "job_description": "Job Posting Title\nEnrollment and Eligibility Subject Matter Expert\nDate\nFriday, January 9, 2026\nCity\nRemote\nCountry\nUnited States\nWorking time\nFull-time\nMaximus is currently hiring for a remote Enrollment and Eligibility S\nubject Matter Expert\n. The\nEnrollment and Eligibility S\nubject Matter Expert\ndelivers consulting services for medium- to long-term engagements, applying a combination of technical expertise, interpersonal skills, and subject matter expertise in SNAP, TANF, and Medicaid policies and processes.\nThis role focuses on the planning, development, delivery, deployment, and oversight of Integrated Eligibility systems to support HHS modernization initiatives.\n*This position is contingent upon contract award. *\nWhy Maximus?\n- 💰\nCompetitive Compensation\n- Quarterly bonuses based on performance included!\n- 🛡️\nComprehensive Insurance Coverage\n- Choose from various plans, including Medical, Dental, Vision, Prescription, and partially funded HSA. Additionally, enjoy Life insurance benefits and discounts on Auto, Home, Renter's, and Pet insurance.\n- 🌟\nFuture Planning\n- Prepare for retirement with our 401K Retirement Savings plan and Company Matching.\n- 🏝️\nPaid Time Off Package\n- Enjoy UTO, Holidays, and sick leave, along with Short and Long Term Disability coverage.\n- 🌱\nHolistic Wellness Support\n- Access resources for physical, emotional, and financial wellness through our Employee Assistance Program (EAP).\n- 🏆\nRecognition Platform\n- Acknowledge and appreciate outstanding employee\ncontributions.\n- 📚\nTuition Reimbursement\n- Invest in your ongoing education and development.\n- 🎁\nEmployee Perks and Discounts\n- Additional benefits and discounts exclusively for employees.\n- 🌟\nMaximus Wellness Program and Resources\n- Access a range of wellness programs and resources tailored to your needs.\n- 📚\nProfessional Development\nOpportunities\n-\nParticipate in training programs, workshops, and conferences.\nEssential Duties and Responsibilities:\n- Collaborate with project managers on various initiatives and projects to track progress and provide support as necessary.\n- Support leadership in ensuring that the project is delivered to specifications, is on time, and within budget.\n- Work closely with management and work groups to create and maintain work plan documents.\n- Track the status and due dates of projects.\n- Manage relationships with project staff responsible for projects.\n- Produce regular weekly and monthly status reports that could include; work plan status, target dates, budget, resource capacity, and other reports as needed.\n- Facilitate regular meetings and reviews.\n- Adhere to contract requirements and comply with all corporate policies and procedures.\n- Provide ad hoc support as needed to project team, developers, and stakeholders as requested by project team.\n- Provide assistance responding to federal partners’ requests for information.\n- Consult on federal or state initiatives or policy changes.\nMinimum Requirements\n- Bachelor's degree in related field.\n- 7-10 years of relevant professional experience required.\n- Equivalent combination of education and experience considered in lieu of degree.\n- Experience with CMS Medicaid Streamline Modular Certification (SMC) and related outcomes and metrics.\n- Experience researching state Medicaid , federal, and state eligibility and enrollment documentation and regulations.\n- Experience defining and designing Medicaid enrollment and reconciliation solutions.\n- Experience speaking with the client/users to understand their specific eligibility business processes\n- Minimum three (3) years’ experience within the last five (5) years in a comparable role on a similar project.\n- Must be willing and able to work a shift that supports the Alaska Standard time zone.\n-\nMust be willing and able to travel 2–4 times per year to Alaska\nHome Office Requirements:\n- Internet speed of 20mbps or higher required (you can test this by going to www.speedtest.net).\n- Connectivity to the internet via either Wi-Fi or Category 5 or 6 ethernet patch cable to the home router.\n- Must currently and permanently reside in the Continental US.\nEEO Statement\nMaximus is an equal opportunity employer.  We evaluate qualified applicants without regard to race, color, religion, sex, age, national origin, disability, veteran status, genetic information and other legally protected characteristics.\nPay Transparency\nMaximus compensation is based on various factors including but not limited to job location, a candidate's education, training, experience, expected quality and quantity of work, required travel (if any), external market and internal value analysis including seniority and merit systems, as well as internal pay alignment. Annual salary is just one component of Maximus's total compensation package. Other rewards may include short- and long-term incentives as well as program-specific awards. Additionally, Maximus provides a variety of benefits to employees, including health insurance coverage, life and disability insurance, a retirement savings plan, paid holidays and paid time off. Compensation ranges may differ based on contract value but will be commensurate with job duties and relevant work experience. An applicant's salary history will not be used in determining compensation. Maximus will comply with regulatory minimum wage rates and exempt salary thresholds in all instances.\nAccommodations\nMaximus provides reasonable accommodations to individuals requiring assistance during any phase of the employment process due to a disability, medical condition, or physical or mental impairment. If you require assistance at any stage of the employment process—including accessing job postings, completing assessments, or participating in interviews,—please contact People Operations at\napplicantaccom@maximus.com\n.\nMinimum Salary\n$\n90,000.00\nMaximum Salary\n$\n110,000.00"},






