# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join, Identity


class WebCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    subject = scrapy.Field()
    description = scrapy.Field()


class WebCrawlerItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
