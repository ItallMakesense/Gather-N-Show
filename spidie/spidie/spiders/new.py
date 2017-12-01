# -*- coding: utf-8 -*-

"""
Jobs.net ?ats? spider
"""

import scrapy
from scrapy.shell import inspect_response
import json
from jobs_crawler.items import Job
from jobs_crawler.spiders.basic import BasicSpider
import logging
import traceback

class HtmlSpider(BasicSpider):
    name = 'html'

    def __init__(self, craft_company_id, url, title_selector=None, link_selector=None, location_selector=None,
                 iframe_selector=None, description_selector=None, pagination_selector=None, use_proxy=None,
                 pagination=None, script=None, follow_job_link=False, traversal_selector=None, job_scraper_id=0,
                 filter_button_selector = None, payload=None, type = 'multiple', priority=0, *args, **kwargs):
        super(HtmlSpider, self).__init__(craft_company_id, url, title_selector=title_selector, link_selector=link_selector,
                 location_selector=location_selector, iframe_selector=iframe_selector, description_selector=description_selector,
                 pagination_selector=pagination_selector, use_proxy=use_proxy, pagination=pagination, script=script, follow_job_link=follow_job_link,
                 job_scraper_id=job_scraper_id, payload=payload, traversal_selector=traversal_selector, priority=priority)
        
        self.craft_company_id = '1313'
        self.job_scraper_id = '1313'

        self.url = 'https://www.jobs.net/jobs/ezcorp/en-us/all-jobs'
        self.title_selector = "[itemprop='title']"
        self.link_selector = "[itemprop='title']"
        self.traversal_selector = None
        self.location_selector = "[itemprop='jobLocation']"
        self.iframe_selector = None
        self.description_selector = '#description'
        self.pagination_selector = '#NextPageArrow'
        self.use_proxy = None
        self.pagination = 'next'
        self.script = None
        self.follow_job_link = True
        self.payload = None
        self.type = 'multiple'
        self.jobs = []
        self.filter_button_selector = None
        self.process_jobs_data_queue = self.env + '.T.process_jobs_data'

    def start_requests(self):
        self.log_job_scraper_info("Start processing url: " + self.url + " with HTML engine")
        if self.payload:
            request = scrapy.Request(url = self.url.encode().decode(), callback=self.parse_job_page, priority = self.priority)
        else:
            request = scrapy.Request(url = self.url.encode().decode(), callback=self.parse_page, priority = self.priority)
        return [request]

    def parse_page(self, response):
        self.log_job_scraper_info("Spider type: " + self.type)
        if self.iframe_selector is not None:
            iframe_url = response.css(self.iframe_selector).xpath('@src').extract_first()
            self.iframe_selector = None
            request = scrapy.Request(url = iframe_url.encode().decode(), callback=self.parse_page, priority = self.priority)
            request.headers['Referer'] = response.url
            yield request
            return

        for next_page_url in self.next_page_urls(response):
            next_page_request = scrapy.Request(url = next_page_url.encode().decode(), callback=self.parse_page, priority = self.priority)
            next_page_request.headers['Referer'] = response.url
            yield next_page_request

        if self.traversal_selector:
            urls = response.css(self.traversal_selector + '::attr(href)').extract()
            temp_jobs = [self.build_job({'link': response.urljoin(url)}) for url in urls]
            try:
                self.process_jobs_data([job.__dict__['_values'] for job in temp_jobs])
            except Exception as error:
                self.log_job_scraper_info("Error processing traversal scraper with HTML engine, Python error: " + str(traceback.format_exc()), log_level = "ERROR")
            return

        titles = self.extract_texts_by_selector(response, self.title_selector)

        locations = None
        if self.location_selector:
            locations = self.extract_texts_by_selector(response, self.location_selector)

        links = None
        if self.link_selector:
            links = response.css(self.link_selector + '::attr(href)').extract()

        descriptions = None
        if self.description_selector:
            descriptions = response.css(self.description_selector).extract()
        try:
            self.process_jobs_data(self.build_items(response, titles, descriptions, locations, links))
        except Exception as error:
            self.log_job_scraper_info("Error processing html scraper, Python error: " + str(traceback.format_exc()), log_level = "ERROR")

    def parse_job_page(self, response):
        self.log_job_scraper_info("Got payload: " + self.payload)
        job_data = json.loads(self.payload)
        if self.title_selector:
            job_data['title'] = response.css(self.title_selector + ' *::text').extract_first()

        if self.location_selector:
            job_data['location'] = response.css(self.location_selector + ' *::text').extract_first()

        if self.description_selector:
            job_data['description'] = response.css(self.description_selector).extract_first()
        try:
            self.process_jobs_data([job_data])
        except Exception as error:
            self.log_job_scraper_info("Error processing job page " + response.url + \
                " with HTML engine\n\nPython error: " + str(traceback.format_exc()), log_level = "ERROR")



    def build_items(self, response, titles = None, descriptions = None, locations = None, links = None):
        count = len(titles)
        if descriptions and len(descriptions) != count:
            raise RuntimeError("Invalid descriptions count")
        if locations and len(locations) != count:
            raise RuntimeError("Invalid locations count")
        if links and len(links) != count:
            raise RuntimeError("Invalid links count")

        items = []
        for i in range(count):
            item = Job(title = titles[i].strip(), craft_company_id = self.craft_company_id, job_scraper_id = self.job_scraper_id)
            if descriptions:
                item['description'] = descriptions[i].strip()
            if locations:
                item['location'] = locations[i].strip()
            if links:
                item['link'] = response.urljoin(links[i].strip()).encode().decode('ascii', 'ignore')
            item['job_scraper_id'] = self.job_scraper_id
            items.append(item)
        return items
