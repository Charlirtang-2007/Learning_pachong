# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AqiItem(scrapy.Item):
    day = scrapy.Field()#日期
    aqi = scrapy.Field()#AQI
    SO2 = scrapy.Field()
    PM10 = scrapy.Field()
    ww = scrapy.Field()#质量等级
    PM2_5 = scrapy.Field()#PM2.5
    no2 = scrapy.Field()
    co = scrapy.Field()
    o3_8h = scrapy.Field()



