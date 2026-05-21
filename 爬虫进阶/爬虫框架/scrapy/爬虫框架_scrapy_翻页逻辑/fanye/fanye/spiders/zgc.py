import scrapy
from fanye.items import ZgcItem

class ZgcSpider(scrapy.Spider):
    name = "zgc"
    allowed_domains = ["detail.zol.com.cn"]
    start_urls = ["https://detail.zol.com.cn/notebook_index/subcate16_0_list_1_0_99_1_0_1.html"]

    def parse(self, response):
        """
        获取主页面单商品url和进行翻页操作
        """
        list_box=response.css('div.content div.list-box div.list-item')
        for li in list_box:
            item = ZgcItem()
            item["link"] = response.urljoin(li.css('div.pro-intro h3 a::attr(href)').get())
            item["name"] = li.css('div.pro-intro h3 a::text').get()
            yield item
        #处理翻页逻辑
        if response.css('div.page-box div.pagebar a.next::text').get()=="下一页":
            yield response.follow((response.css('div.page-box div.pagebar a.next::attr(href)').get()), self.parse)
            page=response.css('div.page-box div.pagebar span.sel::text').get()
            print("当前页数为"+page)






