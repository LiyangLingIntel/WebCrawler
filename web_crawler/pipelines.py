# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import signals
from pydispatch import dispatcher

import pandas as pd
import numpy as np
import os

from web_crawler.settings import CATEGORY


class WebCrawlerPipeline:
    def process_item(self, item, spider):
        return item


class DataSavePipeline:
    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.df = pd.DataFrame(columns=['subject', 'description'])
        self.output_folder = os.path.join(os.getcwd(), 'outputs')
        self.category = ''
        self._block = ''

    @property
    def block(self):
        return self._block

    @block.setter
    def block(self, block_name):
        self._block = block_name.replace(' ', '')

    def save_dataframe(self, spider):
        if self.category:
            save_path = os.path.join(self.output_folder, self.block, f'{self.category}.csv')
            self.df.to_csv(save_path)
            self.df = pd.DataFrame(columns=['subject', 'description'])
            spider.logger.info(f'{self.block}/{self.category} data has been collected.')

    def process_item(self, item, spider):
        new_row = dict(item)
        self.df = self.df.append(new_row, ignore_index=True)

        if self.category != spider.crawler.stats.get_value('category_name'):
            self.save_dataframe(spider)
            self.block = spider.crawler.stats.get_value('category_block')
            self.category = spider.crawler.stats.get_value('category_name')
        return item

    def spider_closed(self, spider):
        output_path = os.path.join(self.output_folder, f'{self.category}.csv')
        self.df.to_csv(output_path)
