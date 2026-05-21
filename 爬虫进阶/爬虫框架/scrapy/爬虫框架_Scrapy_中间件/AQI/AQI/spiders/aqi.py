import scrapy


class AqiSpider(scrapy.Spider):
    name = "aqi"
    allowed_domains = ["aqistudy.cn"]
    start_urls = ["https://www.aqistudy.cn/historydata/monthdata.php?city=%E6%9D%AD%E5%B7%9E"]

    def parse(self, response):
        print(response.text)
