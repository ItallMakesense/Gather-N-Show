"""
Description
"""

import scrapy
from scrapy.crawler import CrawlerProcess


class Spider(scrapy.Spider):
    name = "pie"
    start_urls = ['https://jobs.smartrecruiters.com/WernerEnterprises/743999661236574-dedicated-safety-representative']

    def parse(self, response):
        print(">>>>>", response.css("[itemprop='title']").extract())

if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(Spider)
    process.start()
