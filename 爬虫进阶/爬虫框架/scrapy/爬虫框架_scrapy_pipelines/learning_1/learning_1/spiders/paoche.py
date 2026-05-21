import scrapy


class PaocheSpider(scrapy.Spider):
    name = "paoche"
    allowed_domains = ["tupianzj.com"]
    start_urls = ["https://www.tupianzj.com/bizhi/DNqiche/paoche/list_139_1.html"]

    def parse(self, response):
        print(response.text)
