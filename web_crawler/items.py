# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join, Identity


class CategoryItem(scrapy.Item):
    block = scrapy.Field()
    url = scrapy.Field()


class PostItem(scrapy.Item):
    subject = scrapy.Field()
    description = scrapy.Field()


class WebCrawlerItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
