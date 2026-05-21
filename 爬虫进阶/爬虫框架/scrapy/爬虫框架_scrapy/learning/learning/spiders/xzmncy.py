import scrapy


class XzmncySpider(scrapy.Spider):
    name = "xzmncy" #名字
    allowed_domains = ["www.xzmncy.com"]#限定域名
    start_urls = ["https://www.xzmncy.com/list/58089/"]#起始url

    def parse(self, response): #默认解析函数，直接使用，response对象进行解析即可
       #解析章节url
       book_links = response.css("div#list dl dd a::attr(href)").getall()
       for book_link in book_links:
           yield response.follow(book_link, self.parse_book) #生成一个新的 Request 对象，目标 URL 是 book_link（不用你自己拼）

    def parse_book(self, response):
        yield {
            "title": response.css("div#read div.readbar div.bookname h1::text").get(),
            "content": '\n'.join(response.css("div#read div.readbar div#htmlContent p::text").getall()),
        }