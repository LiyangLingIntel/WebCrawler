import scrapy
from scrapy import Selector
from scrapy import signals
from scrapy.http import Request
from pydispatch import dispatcher
from urllib import parse

from web_crawler.items import WebCrawlerItem, WebCrawlerItemLoader
from web_crawler.settings import CATEGORY
from utils.string_helper import category_to_suffix


class CommunitySpider(scrapy.Spider):
    name = 'intel_community'
    allowed_domains = ['community.intel.com']
    start_urls = [f'https://community.intel.com/t5/{CATEGORY}/bd-p/{category_to_suffix(CATEGORY)}']
    category_root = f'https://community.intel.com/t5/{CATEGORY}'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fail_urls = []
        dispatcher.connect(self.handle_spider_closed, signals.spider_closed)

    def handle_spider_closed(self, spider, reason):
        self.crawler.stats.set_value("failed_urls", ",".join(self.fail_urls))

    def parse(self, response):
        post_nodes = response.xpath('//a[@class="page-link lia-link-navigation lia-custom-event"]')
        for post_node in post_nodes:
            post_suffix = post_node.xpath('./@href').get('')
            post_url = parse.urljoin(self.category_root, post_suffix)
            yield Request(url=post_url, callback=self.parse_post)

        next_url = response.xpath('//a[@rel="next"]/@href').get('')
        next_url = parse.urljoin(self.start_urls[0], next_url)
        yield Request(url=next_url, callback=self.parse)

    def parse_post(self, response):

        item_loader = WebCrawlerItemLoader(item=WebCrawlerItem())

        class_question_div = 'lia-quilt lia-quilt-forum-message lia-quilt-layout-forum-topic-message-support'
        question_node_text = response.xpath(f'//div[@class="{class_question_div}"]').get('')
        question_node = Selector(text=question_node_text)

        class_subject = 'lia-message-subject'
        subject = question_node.xpath(f'.//div[@class="{class_subject}"]/text()').get('').strip()
        item_loader.add_value('subject', subject)

        class_description = 'lia-message-body-content'
        content_nodes_text = question_node.xpath(f'.//div[@class="{class_description}"]').get('')
        contents = Selector(text=content_nodes_text).xpath('//p/text() | //h1/text() | //h2/text() | //h3/text()')
        description = ''
        for content in contents:
            desc_text = content.get().strip()  # Selector.get() v.s. SelectorList.get(default=None)
            description += desc_text
            description += ' '
        item_loader.add_value('description', description)

        yield item_loader.load_item()
