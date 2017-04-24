import unittest
from scrapytest.spiders import getdata
from responses import test_response

class TestSpider(unittest.TestCase):
    
    def directory(self):
        self.directory = getdata.DirectorySpider()

    def test_parse(self):
        response = self.directory.parse(test_response('http://anweb.pro/govpredict.html'))
        self.assertTrue(response)
        
if __name__ == '__main__':
    unittest.main(exit=False)