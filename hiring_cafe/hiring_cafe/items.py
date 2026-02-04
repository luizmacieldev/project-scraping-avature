# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AvatureJobItem(scrapy.Item):
    job_id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()
    work_location = scrapy.Field()
    posted_date = scrapy.Field()
    business_area = scrapy.Field()
    duration = scrapy.Field()
    job_description = scrapy.Field()
    extracted_at = scrapy.Field()
