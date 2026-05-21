# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FanyeItem(scrapy.Item):
    name = scrapy.Field()
    tiaojian = scrapy.Field()
    job = scrapy.Field()
    workPlaceName= scrapy.Field()
class ZgcItem(scrapy.Item):
    link = scrapy.Field()
    name = scrapy.Field()
