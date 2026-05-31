import scrapy

city=input("请输入城市")
class AqiSpider(scrapy.Spider):
    name = "aqi"
    allowed_domains = ["aqistudy.cn"]
    start_urls = [f"https://www.aqistudy.cn/historydata/monthdata.php?city={city}"]

    def parse(self, response):
        # 月份列表
        month_urls=response.css('ul.unstyled1 li a::attr(href)').getall()
        for month_url in month_urls:
            yield response.follow(month_url,self.aqi_parse,meta={'selenium':True})# 这里要用selenium渲染
    def aqi_parse(self,response):
        print(response.text)

