# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
import random
# useful for handling different item types with a single interface



class FakeUserAgentMiddleware:
    ua = UserAgent()  # 类变量，只加载一次
    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', self.ua.chrome)
        spider.logger.debug(f'请求头: {request.headers}')


class RandomProxyMiddleware:
    def __init__(self, proxy_list):
        self.proxy_list = proxy_list

    @classmethod
    def from_crawler(cls, crawler):
        # 从 settings.py 中读取代理列表
        proxy_list = crawler.settings.getlist('PROXY_LIST')
        return cls(proxy_list)

    def process_request(self, request, spider):
        # 为每个请求随机选择一个代理
        proxy = random.choice(self.proxy_list)
        request.meta['proxy'] = proxy if proxy.startswith(('http://', 'https://')) else 'http://' + proxy
        spider.logger.debug(f'使用代理: {proxy}')

