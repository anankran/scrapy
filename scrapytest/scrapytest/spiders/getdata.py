import scrapy
import sys

from scrapy.crawler import CrawlerProcess
from scrapy.http import Request, FormRequest, Response, TextResponse, HtmlResponse, Headers

class ScrapyTest(scrapy.Spider):

    name = 'scrapytestspider'

    # Creates list to loop over page
    pages = [range(1, 550, 15)]
    actual_page = 1

    allowed_domains = [ 'fara.gov', 'anweb.pro' ]

    # Make GET requests to generate Cookie
    start_urls = [
        'https://www.fara.gov/quick-search.html'
    ]

    # Uses response to make POST requests using cookie
    def parse(self, response):
        if response.headers.getlist('Set-Cookie'):
            cookie = str( response.headers.getlist('Set-Cookie') ).split('; ')[0].split('=')[1]
            for page in self.pages:
                actual_page = page;
                headers = {
                            'Cookie' : cookie,
                            'Content-Type' : 'application/x-www-form-urlencoded'
                          }
                data = {
                        'p_request' : 'APXWGT',
                        'p_instance' : '11307111314125',
                        'p_flow_id' : '171',
                        'p_flow_step_id' : '130',
                        'p_widget_num_return' : '15',
                        'p_widget_name' : 'worksheet',
                        'p_widget_mod' : 'ACTION',
                        'p_widget_action' : 'PAGE',
                        'p_widget_action_mod' : 'pgR_min_row=' + str(page) + 'max_rows=15rows_fetched=15',
                        'x01' : '80340213897823017',
                        'x02' : '80341508791823021'
                        }
                meta = {
                        'dont_redirect': True,
                        'handle_httpstatus_list': [302]
                        }
                request = scrapy.FormRequest('http://anweb.pro/fake.html', headers=headers, formdata=data, meta=meta, callback=self.parse)
            yield request

    # Start extracting data from to HTML response
    def parse_page1(self, response):
        values = {}
        i = self.actual_page
        for id_header, header in enumerate(response.xpath('//table[@class="apexir_WORKSHEET_DATA"]//th[@class="apexir_REPEAT_HEADING"]')):
            container_name = header.xpath('@id').extract()[0]
            country = header.xpath('//th[@id="' + container_name + '"]/span/text()').extract()[0]

            for id_row, row in enumerate(response.xpath('//table[@class="apexir_WORKSHEET_DATA"]//tr[@class="odd"]//td[@headers="LINK ' + container_name + '"] | //table[@class="apexir_WORKSHEET_DATA"]//tr[@class="even"]//td[@headers="LINK ' + container_name + '"]')):
                url = 'https://efile.fara.gov/pls/apex/' + row.xpath('//td[@headers="LINK ' + container_name + '"]/a/@href').extract()[id_row]
                #print(response.xpath('//table[@class="apexir_WORKSHEET_DATA"]//tr[@class="odd"]//td[@headers="STATE ' + container_name + '"]/text()'))
                state = ''
                reg_num = row.xpath('//td[@headers="REG_NUMBER ' + container_name + '"]/text()').extract()[id_row]
                address = row.xpath('//td[@headers="ADDRESS_1 ' + container_name + '"]/text()').extract()[id_row]
                foreign_principal = row.xpath('//td[@headers="FP_NAME ' + container_name + '"]/text()').extract()[id_row]
                date = row.xpath('//td[@headers="FP_REG_DATE ' + container_name + '"]/text()').extract()[id_row]
                registrant = row.xpath('//td[@headers="REGISTRANT_NAME ' + container_name + '"]/text()').extract()[id_row]
                doclink = scrapy.Request(url, callback=self.parse_page2)

                values[i] = { "url" : url, "country" : country, "state" : state, "reg_num" : reg_num, "address" : address, "foreign_principal" : foreign_principal, "date" : date, "registrant" : registrant }
                i = i + 1
        yield values

    # Make GET request to extract data from the unique page
    def parse_page2(self, response):
        print(response.body)
        #doclink = response.xpath('//td[@headers="DOCLINK"]/text()').extract()
        #print(doclink)
        #yield [join(doclink)] 

process = CrawlerProcess()
process.crawl(ScrapyTest)
process.start()
