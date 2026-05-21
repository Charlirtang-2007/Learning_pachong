import requests
import random
from parsel import Selector
import csv
import time
from fake_useragent import UserAgent #可以使用 fake-useragent 库随机生成不同浏览器的 UA
url = "https://www.xzmncy.com/list/58017/"#这里设置一个，url对象，方便后续使用
ua = UserAgent() #设置ua对象
headers = {'User-Agent': ua.random}  # 每次随机一个 UA
timeout=(3,5)
#延迟添加
#建立一个列表,用来存数据
data_list=[]
delay = random.uniform(1, 3)
print(f"等待 {delay:.2f} 秒后继续...")
time.sleep(delay)
#发送请求
response = requests.get(url, headers=headers, timeout=timeout)
#解析数据
selector = Selector(text=response.text)
# dict={} 不要用内置函数名称
id_list=selector.css('div#list dl')
for item in id_list:
    hrefs = item.css('dd a::attr(href)').getall()
    titles = item.css('dd a::text').getall()
    for title,href in zip(titles,hrefs):#zip函数很好用，同时遍历返回元组的形式
        data_list.append({'title': title,'url': f"https://www.xzmncy.com{href}"})
#储存数据
with open('xzmncy.csv', 'w+', newline='',encoding='utf-8-sig') as f:
    fieldnames = ['title','url'] #指定字段顺序，指定字典的键顺序，也作为表头。
    writer = csv.DictWriter(f,fieldnames=fieldnames)
    writer.writeheader() #写入表头
    writer.writerows(data_list) #写入数据

