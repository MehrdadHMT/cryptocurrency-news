from django.core.management.base import BaseCommand
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging

from crawling.crawling.spiders.ramzarznews import RamzarzNewsSpider
from crawling.crawling.spiders.arzdigital import ArzdigitalSpider
from crawling.crawling import settings as my_crawler_settings


class Command(BaseCommand):
    help = "Release the spiders"

    def handle(self, *args, **options):
        configure_logging()
        crawler_settings = Settings()

        # Correct directory problems to access crawler settings from outside its root directory
        my_crawler_settings.SPIDER_MODULES = ['crawling.crawling.spiders']
        my_crawler_settings.NEWSPIDER_MODULE = 'crawling.crawling.spiders'
        my_crawler_settings.ITEM_PIPELINES = {'crawling.crawling.pipelines.CcNewsCrawlingPipeline': 300}
        crawler_settings.setmodule(my_crawler_settings)

        runner = CrawlerRunner(settings=crawler_settings)

        runner.crawl(RamzarzNewsSpider)
        runner.crawl(ArzdigitalSpider)
        d = runner.join()
        d.addBoth(lambda _: reactor.stop())

        reactor.run()   # the script will block here until all crawling jobs are finished
