import scrapy
import sys

from scrapy.selector import Selector
from scrapy.http import Request, FormRequest, Response, TextResponse, HtmlResponse, Headers

class ScrapyTest(scrapy.Spider):

    name = 'scrapytest'
    pages = [range(1, 550, 15)]

    def start_requests(self):
        for page in self.pages:
            headers = {
                        'Cookie' : 'ORA_WWV_APP_171=ORA_WWV-qoimWYFQq/DecvF8M2SiuXIs; _ga=GA1.2.1799795598.1492437953; TS013766ce=016889935cb1157b4869984d7b321c719cfe152bfa5c8c847ac71cfbec90946f06d04fc942d1a04a4acf9bf002ecafbacc7f244738'
                      }
            #pagination = 'pgR_min_row='+page+'max_rows=15rows_fetched=15'
            data = {
                    'p_request' : 'APXWGT',
                    'p_instance' : '8406264081358',
                    'p_flow_id' : '171',
                    'p_flow_step_id' : '130',
                    'p_widget_num_return' : '15',
                    'p_widget_name' : 'worksheet',
                    'p_widget_mod' : 'ACTION',
                    'p_widget_action' : 'PAGE',
                    'p_widget_action_mod' : 'pgR_min_row=1max_rows=15rows_fetched=15',
                    'x01' : '80340213897823017',
                    'x02' : '80341508791823021'
                    }
            yield scrapy.FormRequest('https://efile.fara.gov/pls/apex/wwv_flow.show', headers=headers, formdata=data, meta = {'dont_redirect': True,'handle_httpstatus_list': [302]}, callback=self.parse)

    def parse(self,response):
        hxs = Selector(response)
        rows = hxs.xpath('//table[@class=apexir_WORKSHEET_DATA]//tr')

        json = '{'
        for row in rows:
            json += '{'
            if (node.xpath("@class") == 'even') or (node.xpath("@class") == 'odd'):
                url = row.xpath('//td[@headers=LINK]/a[@href]')
                state = row.xpath('//td[@headers=STATE]/text()')
                reg_num = row.xpath('//td[@headers=REG_NUMBER]/text()')
                address = row.xpath('//td[@headers=ADDRESS_1]/text()')
                foreign_principal = row.xpath('//td[@headers=FP_NAME]/text()')
                date = row.xpath('//td[@headers=FP_REG_DATE]/text()')
                registrant = row.xpath('//td[@headers=REGISTRANT_NAME]/text()')
                exhibit_url = row.xpath('//td[@headers=LINK]/text()')
            else:
                country = row.xpath('//span[@class=apex_break_headers]/text()')
            json += ' "url" : "' + url + '" }'
            json += ' "country" : "' + country + '" }'
            json += ' "state" : " ' + state + ' " }'
            json += ' "reg_num" : " ' + reg_num + ' " }'
            json += ' "address" : " ' + address + ' " }'
            json += ' "foreign_principal" : " ' + foreign_principal + ' " }'
            json += ' "date" : " ' + date + ' " }'
            json += ' "registrant" : " ' + registrant + ' " }'
        json += '}'
        print(json)