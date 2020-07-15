import scrapy
from scrapy import Selector
from scrapy import signals
from scrapy.http import Request
from pydispatch import dispatcher
from urllib import parse

from web_crawler.items import CategoryItem, PostItem, WebCrawlerItemLoader
from web_crawler.settings import CATEGORY
from utils.string_helper import category_to_suffix, remove_blank


class CommunitySpider(scrapy.Spider):
    name = 'intel_community_crawler'
    allowed_domains = ['community.intel.com']
    start_urls = ['https://community.intel.com/']
    category_root = f'https://community.intel.com/t5/{CATEGORY}'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fail_urls = []
        dispatcher.connect(self.handle_spider_closed, signals.spider_closed)

        self.cate_nodes = ['lia-tree-node-9', 'lia-tree-node-37', 'lia-tree-node-87']

    def handle_spider_closed(self, spider, reason):
        self.crawler.stats.set_value("failed_urls", ",".join(self.fail_urls))

    def parse(self, response):
        for node_id in self.cate_nodes:
            node_prefix = f'"{node_id} lia-list-tree-toggle-node"'
            category_block = response.xpath(f'//li[starts-with(@class, {node_prefix})]')

            # send current category block to spider
            block_name = category_block.xpath('./a/text()').get()
            self.crawler.stats.set_value('category_block', block_name)

            category_suffixes = category_block.xpath('.//a/@href').getall()

            category_suffixes = [suf for suf in category_suffixes if self._is_category_url(suf)]
            for category_suffix in category_suffixes:
                # send current category name to spider
                self.crawler.stats.set_value('category_name', category_suffix.split('/')[-1])
                category_url = parse.urljoin(self.start_urls[0], category_suffix)
                yield Request(url=category_url, callback=self.parse_category)

    def parse_block(self, response):
        pass

    def parse_category(self, response):
        post_nodes = response.xpath('//a[@class="page-link lia-link-navigation lia-custom-event"]')
        for post_node in post_nodes:
            post_suffix = post_node.xpath('./@href').get('')
            post_url = parse.urljoin(self.category_root, post_suffix)
            yield Request(url=post_url, callback=self.parse_post)

        next_url = response.xpath('//a[@rel="next"]/@href').get('')
        next_url = parse.urljoin(self.start_urls[0], next_url)
        yield Request(url=next_url, callback=self.parse)

    def parse_post(self, response):
        item_loader = WebCrawlerItemLoader(item=CategoryItem())

        class_question_div = 'lia-quilt lia-quilt-forum-message lia-quilt-layout-forum-topic-message-support'
        question_node_text = response.xpath(f'//div[@class="{class_question_div}"]').get('')
        question_node = Selector(text=question_node_text)

        class_subject = 'lia-message-subject'
        subject = question_node.xpath(f'.//div[@class="{class_subject}"]/text()').get('').strip()
        item_loader.add_value('subject', subject)

        class_description = 'lia-message-body-content'
        content_nodes_text = question_node.xpath(f'.//div[@class="{class_description}"]').get('')
        contents = Selector(text=content_nodes_text).xpath('.//*[not(self::code)]/text()')
        description = ''
        for content in contents:
            desc_text = content.get().strip()  # Selector.get() v.s. SelectorList.get(default=None)
            description += remove_blank(desc_text)
        item_loader.add_value('description', description)

        yield item_loader.load_item()

    def _is_category_url(self, url):
        url_tokens = url.split('/')
        if len(url_tokens) < 2 or url_tokens[-2] != 'bd-p':
            return False
        else:
            return True
