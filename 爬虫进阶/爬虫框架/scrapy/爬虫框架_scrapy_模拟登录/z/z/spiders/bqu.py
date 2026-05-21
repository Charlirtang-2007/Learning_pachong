import re
import scrapy
class BquSpider(scrapy.Spider):
    name = "bqu"
    allowed_domains = ["www.bequke.com"]


    def start_requests(self):
        yield scrapy.Request(
            url='https://www.bequke.com',
            callback=self.parse,
            errback=self.errback,
        )

    def errback(self, failure):
        print(f"请求失败: {failure.value}")
        print(f"类型: {failure.type}")

    def parse(self, response):
        data = {
            'username': '',
            'password': '',
            'action': 'login',
            'jumpurl': '/bookcase',
            'submit': '',
        }
        yield scrapy.FormRequest(url='https://www.bequke.com/login',formdata=data,callback=self.after_login)
    def after_login(self, response):
        print(f'after_login{response.status}')
        print(response.css('title::text').extract())
