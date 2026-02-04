import scrapy
from urllib.parse import urljoin
from hiring_cafe.items import AvatureJobItem
from hiring_cafe.common.functions import load_avature_sites, normalize_key
import re
from datetime import datetime, timezone

AVATURE_SITES = load_avature_sites()

CUSTOM_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
}

ALLOWED_FIELDS = {
    "work_location",
    "posted_date",
    "job_id",
    "business_area",
    "duration",
}

class AvatureSpider(scrapy.Spider):
    name = "avature_spider"
    allowed_domains = ["avature.net"]
    
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': CUSTOM_HEADERS,
        'COOKIES_ENABLED': True,
        'CONCURRENT_REQUESTS': 2,
        'DOWNLOAD_DELAY': 1,
    }
    
    def start_requests(self):
        for site in AVATURE_SITES:
            site_name = site["name"]
            base_url = site["base_url"]
            self.logger.info(f"Starting scraping for site: {site_name}")
            
            yield scrapy.Request(
                base_url,
                callback=self.parse_listing,
                meta={
                    "site_name": site_name,
                    "base_domain": base_url.split("/careers")[0]
                },
                headers=CUSTOM_HEADERS
            )
    
    def parse_listing(self, response):
        site_name = response.meta["site_name"]
        base_domain = response.meta["base_domain"]
        
        job_links = response.css(
            "article.article--result .article__header__text__title a"
        )
        self.logger.info(f"{site_name}: found {len(job_links)} jobs on page")
        
        for a in job_links:
            href = a.attrib.get("href")
            title = a.css("::text").get(default="").strip()
            
            if not href:
                continue
            
            if href.startswith("/"):
                href = urljoin(base_domain, href)
            
            yield scrapy.Request(
                href,
                callback=self.parse_job,
                meta={
                    "site_name": site_name,
                    "title": title,
                    "url": href
                },
            )
        
        next_page = response.css("a.paginationNextLink::attr(href)").get()
        if next_page:
            next_page = urljoin(base_domain, next_page)
            self.logger.info(f"Following next page for {site_name}: {next_page}")
            yield scrapy.Request(
                next_page,
                callback=self.parse_listing,
                meta={
                    "site_name": site_name,
                    "base_domain": base_domain
                },
            )
    
    def parse_job(self, response):
        site_name = response.meta["site_name"]
        title = response.meta["title"]
        url = response.meta["url"]
        
        # --- Job ID extraction ---
        match = re.search(r"\d+", url)
        if not match:
            self.logger.warning(f"Job ID not found in URL, skipping job: {url}")
            return
        
        job_id = match.group()
        
        # --- Fields extraction ---
        extracted_fields = {}
        fields = response.css(".article__content__view__field")
        
        for field in fields:
            label = field.css(
                ".article__content__view__field__label::text"
            ).get()
            
            value = field.css(
                ".article__content__view__field__value::text"
            ).get()
            
            if not value:
                continue
            
            if not label and ":" in value:
                raw_label, raw_value = value.split(":", 1)
                key = normalize_key(raw_label)
                if key in ALLOWED_FIELDS:
                    extracted_fields[key] = raw_value.strip()
                continue
            
            if label:
                key = normalize_key(label)
                if key in ALLOWED_FIELDS:
                    extracted_fields[key] = value.strip()
        

                # Seleciona todo o conteúdo dentro de article__content__view
        text_nodes = response.css(
            ".article__content__view ::text"
        ).getall()

        # Limpar espaços e quebras
        cleaned = [t.strip() for t in text_nodes if t.strip()]

        # Remover linhas finais de UI indesejadas
        lines_to_remove = {"share this job", "facebook", "x", "linkedin", "apply", "email", "share"}
        while cleaned:
            last_line = cleaned[-1].lower().rstrip(":")
            if any(kw in last_line for kw in lines_to_remove):
                cleaned.pop()
            else:
                break

        # Juntar tudo em uma string final
        description = " ".join(cleaned)

        
        # --- Create item only at the end ---
        job = AvatureJobItem()
        job["title"] = title
        job["url"] = url
        job["source"] = site_name
        job["job_id"] = job_id
        job["extracted_at"] = datetime.now(
            timezone.utc
        ).isoformat()
        
        for key, value in extracted_fields.items():
            job[key] = value
        
        if description:
            job["job_description"] = description
        
        yield job