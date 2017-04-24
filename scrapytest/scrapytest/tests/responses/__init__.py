import os
from scrapy.http import Response, Request

def test_response(url):
    
    request = scrapy.Response(url=url)
    request.encoding = 'utf-8'
    return request