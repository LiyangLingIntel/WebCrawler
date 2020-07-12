import scrapy
from scrapy.http import Request
from urllib import parse


class CommunitySpider(scrapy.spiders):
    name = 'intel_community'
    allowed_domains = ['community.intel.com']
    start_urls = ['https://community.intel.com/t5/FPGA-Intellectual-Property/bd-p/fpga-intellectual-property']

    def parse(self, response):
        pass

    def parse_post(self, response):
        pass
