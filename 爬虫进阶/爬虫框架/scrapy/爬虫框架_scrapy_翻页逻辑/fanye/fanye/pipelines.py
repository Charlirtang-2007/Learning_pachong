# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from os import write

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import json
class FanyePipeline:
    def open_spider(self):
        self.f=open('fanye.json','a',encoding='utf-8')
    def close_spider(self):
        if self.f:
            self.f.close()
    def process_item(self, item):
        shuju={
            '职业名字':item["name"] ,
            '职业条件':item["tiaojian"] ,
            '职业内容':item["job"] ,
            '工作地点':item["workPlaceName"]
        }
        if shuju:
            self.f.write(json.dumps(shuju,ensure_ascii=False))
class ZgcPipeline:
    def process_item(self, item):
        print(item['link'])

        return item

