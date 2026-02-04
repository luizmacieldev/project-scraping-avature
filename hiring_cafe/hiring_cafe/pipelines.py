from scrapy.exceptions import DropItem


class HiringCafePipeline:
    def process_item(self, item, spider):
        return item


class DeduplicateJobPipeline:
    def __init__(self):
        self.seen_job_ids = set()

    def process_item(self, item, spider):
        job_id = item.get("job_id")

        if not job_id:
            raise DropItem("Item without job_id")

        if job_id in self.seen_job_ids:
            spider.logger.info(f"Duplicate job skipped: {job_id}")
            raise DropItem(f"Duplicate job_id: {job_id}")

        self.seen_job_ids.add(job_id)
        return item
