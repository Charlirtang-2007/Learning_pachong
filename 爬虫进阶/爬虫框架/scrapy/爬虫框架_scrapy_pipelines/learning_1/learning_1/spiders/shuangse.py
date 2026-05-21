import scrapy
from learning_1.items import Learning1Item #从learning_1包里的items文件导入Learning1Item类
class ShuangseSpider(scrapy.Spider):
    name = "shuangse"
    allowed_domains = ["500.com"]
    start_urls = ["https://datachart.500.com/ssq/"]

    def parse(self, response):
        bodys=response.css('tbody#tdata tr')
        for body in bodys:
            if body.css('td::text').get() is None:#过滤
                continue
            red_ball=body.css('.chartBall01::text').getall()
            bule_ball=body.css('.chartBall02::text').get()
            qihao=body.xpath('./td[@align="center"]/text()').get()#记得加“./”代表当前路径
            caipaio=Learning1Item() #定义字典
            caipaio['red_ball']=red_ball
            caipaio['bule_ball']=bule_ball
            caipaio['qihao']=qihao
            yield caipaio




