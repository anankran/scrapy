import scrapy

from scrapy.crawler import CrawlerProcess
from scrapy.http import Request, Response

class TestScrapy(scrapy.Spider):

    name = 'scrapytestspider'
    pages = [range(1, 10, 1)]
    allowed_domains = [ 'stackoverflow.com' ]

    def start_requests(self):
        for page in self.pages:
            yield scrapy.Request('http://stackoverflow.com/questions/tagged/python?page=' + str(page) + '&sort=newest&pagesize=50', callback=self.parse)

    def parse(self, response):
        for question in response.css('div.question-summary'):
            title = question.css('div.question-summary h3 a::text').extract_first()
            link = question.css('div.question-summary h3 a::attr(href)').extract_first()
            yield {'title': title, 'link': 'http://stackoverflow.com/' + link}

#process = CrawlerProcess()
#process.crawl(TestScrapy)
#process.start()
