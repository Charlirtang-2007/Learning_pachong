from typing import Iterable, Any

import scrapy


class BzSpider(scrapy.Spider):
    name = "bz"
    allowed_domains = ["www.haowallpaper.com"]
    start_urls = ["https://www.haowallpaper.com/userProfile/"]
    def start_requests(self) -> Iterable[Any]:
        url=self.start_urls[0]
        temp=""""""
        cookies={data.split('=')[0] :data.split('=')[-1] for data in  temp.split(';')}#改写成字典
        yield scrapy.Request(url=url,cookies=cookies,callback=self.parse)

    def parse(self, response):
        print(response.text)
        print(response.css('div.user-address span::text').get())
