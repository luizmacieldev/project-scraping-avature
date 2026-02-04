from scrapy.exceptions import DropItem


class HiringCafePipeline:
    def process_item(self, item, spider):
        return item


from scrapy.exceptions import DropItem

class HiringCafePipeline:
    """
    A basic Scrapy pipeline for processing scraped items.

    Purpose:
        - Acts as a placeholder for item processing.
        - Can be extended for tasks such as data cleaning, validation, 
          transformation, or sending data to databases.

    Methods:
        process_item(item, spider):
            Processes a single scraped item and returns it unchanged.

    Parameters:
        item (dict or Item): The scraped item yielded by the spider.
        spider (scrapy.Spider): The spider that produced the item.

    Returns:
        dict or Item: The same item, unmodified.
    """
    def process_item(self, item, spider):
        return item


class DeduplicateJobPipeline:
    """
    A Scrapy pipeline to deduplicate job items based on 'job_id'.

    Purpose:
        - Ensures that each job is processed only once.
        - Prevents duplicates in the output dataset by tracking 'job_id'.
        - Logs duplicate items for auditing.

    Attributes:
        seen_job_ids (set): A set that stores all job IDs already processed.

    Methods:
        process_item(item, spider):
            Processes a single scraped item and removes duplicates.

    Parameters:
        item (dict or Item): The scraped job item yielded by the spider.
        spider (scrapy.Spider): The spider that produced the item.

    Raises:
        DropItem: If the item has no 'job_id' or is a duplicate.

    Returns:
        dict or Item: The processed item if it is unique.
    """
    def __init__(self):
        self.seen_job_ids = set()

    def process_item(self, item, spider):
        """
        Checks the 'job_id' of the item and drops duplicates.

        Steps:
            1. Extract the 'job_id' from the item.
            2. If 'job_id' is missing, raise DropItem.
            3. If 'job_id' has already been seen, log and raise DropItem.
            4. If 'job_id' is new, add it to seen_job_ids and return the item.

        Parameters:
            item (dict or Item): The job item to process.
            spider (scrapy.Spider): The spider that produced the item.

        Raises:
            DropItem: If the item has no 'job_id' or is a duplicate.

        Returns:
            dict or Item: The original item if unique.
        """
        job_id = item.get("job_id")

        if not job_id:
            raise DropItem("Item without job_id")

        if job_id in self.seen_job_ids:
            spider.logger.info(f"Duplicate job skipped: {job_id}")
            raise DropItem(f"Duplicate job_id: {job_id}")

        self.seen_job_ids.add(job_id)
        return item
