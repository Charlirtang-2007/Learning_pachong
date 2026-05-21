# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from os import makedirs
import csv
import os
import pymysql
from learning_1.settings import MYSQL
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
"""
数据存储的方案：
            1.数据存储在csv文件中
            2MySQL中
            3mongodb
            4文件存储
"""
class CsvPipeline:
    def open_spider(self):#通过（self）.传数据，类似继承
        folder = "D:/数据csv"  # 根目录
        makedirs(folder, exist_ok=True)  # 创建目录，如果存在，也不报错
        self.file_name = os.path.join(folder, "双色球.csv")
        # 判断文件是否已存在且有内容
        self.file_exists = os.path.isfile(self.file_name) and os.path.getsize(self.file_name) > 0
        self.f = open(self.file_name, "a", newline="", encoding="utf-8")
        self.fieldnames = ['期号', '红球', '蓝球']
        self.writer = csv.DictWriter(self.f, fieldnames=self.fieldnames)

    def close_spider(self):
        if self.f:
            self.f.close()
    def process_item(self, item):

        data={"期号":item['qihao'],"红球":"_".join(item['red_ball']),"蓝球":item['bule_ball']}
        # 检查文件是否存在且非空（决定是否写表头）
        if not self.file_exists:
            self.writer.writeheader()
            self.file_exists = True  # 只写一次表头
        self.writer.writerow(data)      # 写入一行数据（注意是 writerow，不是 writerows）
#             # f.write(f"{item['qihao']},{'_'.join(item['red_ball'])},{item['bule_ball']}")
# #'_'.join(item['red_ball']),因为红球是列表，要把它转成字符串，这里用，join来写
#         print(item['qihao'])
        return item

class MysqlPipeline:
    def open_spider(self):
        self.conn=pymysql.connect(host=MYSQL['host'],user=MYSQL['user'],password=MYSQL['password'],db=MYSQL['db'],charset=MYSQL['charset'])#链接，数据库
        self.cursor=self.conn.cursor()#创建游标
    def process_item(self, item):
        sql = "insert into caipiao(期号,红球,蓝球) values(%s,%s,%s)"
        # 写入命令和数据
        self.cursor.execute(sql, (item['qihao'],"_".join(item['red_ball']),item['bule_ball']))
        self.conn.commit()
    def close_spider(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

