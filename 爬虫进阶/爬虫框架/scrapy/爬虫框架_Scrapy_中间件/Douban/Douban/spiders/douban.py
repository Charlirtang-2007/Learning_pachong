import scrapy


class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["douban.com"]
    start_urls = ["https://www.douban.com/doulist/45012218/"]

    def parse(self, response):
        for i in response.css("div.bd.doulist-subject div.title a"):
            url=i.css('::attr(href)').extract_first()
            if url:
                yield  response.follow(url,callback=self.aftert_parse)
            else:
                print("None")
    def aftert_parse(self, response):
        link=response.xpath('//form[@id="sec"]/input[@id="red"]/@value').get()
        if link is not None:
            yield response.follow(link,callback=self.text_parse)
        else:
            print("None")
    def text_parse(self,response):
        print(response.css("title::text").extract_first())

