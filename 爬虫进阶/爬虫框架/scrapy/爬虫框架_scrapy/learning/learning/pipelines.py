# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

#setting里启动
import os
class LearningPipeline:
    def process_item(self, item):#处理数据的特定方法
        folder="D:/小说/xzmncy"
        os.makedirs(folder, exist_ok=True)
        safe_title=item['title'].replace("/", "_").replace("\\", "_").replace(":", "_")
        # 拼接完整路径
        filename = os.path.join(folder, f"{safe_title}.txt")
        print(filename)
        with open(filename, "w",encoding="utf-8") as f:
            f.write(item['content'])
        return item
