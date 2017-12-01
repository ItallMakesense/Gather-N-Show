"""
Description
"""

import scrapy


class SECSpider(scrapy.Spider):
    name = "report"
    start_urls = ['https://www.sec.gov/edgar/searchedgar/companysearch.html']

    # cik = '0001326801'
    # filing = '10-K'
    # fil_format = 'Interactive Data'
    # doc_phrase = 'View Excel Document'

    def parse(self, response):
        """ """
        # Need to extract #fast-search from response
        # Maybe response.css('form.companySearchForm') ?
        # Or response.css('form[id='fast-search'] ....
        return scrapy.FormRequest.from_response(
            response,
            formid='fast-search',
            formdata={
                'CIK': self.cik,
                'owner': 'exclude',
                'action': 'getcompany',
                'Find': 'Search',
                },
            callback=self.cik_page
        )

    def cik_page(self, response):
        """ """
        for sel in response.css('tr'):
            if self.filing in sel.css('::text').extract():
                for link in sel.css('a'):
                    if self.fil_format in link.css('::text').extract_first():
                        next_page = link.css('a::attr(href)').extract_first()
                        return response.follow(next_page, callback=self.filing_page)

    def filing_page(self, response):
        """ """
        for sel in response.css('a'):
            if self.doc_phrase in sel.css('::text').extract():
                doc_page = sel.css('a::attr(href)').extract_first()
                print(doc_page)
                return response.follow(doc_page, callback=self.download)

    def download(self, response):
        """ """
        path = response.url.split('/')[-1]
        with open(path, 'wb') as file:
            file.write(response.body)
