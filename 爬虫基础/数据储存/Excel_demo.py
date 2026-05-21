import pandas as pd
import requests
import random
from parsel import Selector
import time
from fake_useragent import UserAgent #可以使用 fake-useragent 库随机生成不同浏览器的 UA
url = "https://www.xzmncy.com/list/58017/"#这里设置一个，url对象，方便后续使用
ua = UserAgent() #设置ua对象
# headers = {'User-Agent': ua.random}  # 每次随机一个 UA
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
timeout=(3,5)
#延迟添加
#建立一个列表,用来存数据
data_list=[]
delay = random.uniform(1, 3)
print(f"等待 {delay:.2f} 秒后继续...")
time.sleep(delay)
#发送请求
response = requests.get(url, headers=headers, timeout=timeout)
print(response.text)
#解析数据
selector = Selector(text=response.text)
# dict={} 不要用内置函数名称
id_list=selector.css('ul.chapter,div#list')
for item in id_list:
    hrefs = item.css('li a::attr(href),dl dd a::attr(href)').getall()
    titles = item.css('li a::text,dl dd a::text').getall()
    for title,href in zip(titles,hrefs):#zip函数很好用，同时遍历返回元组的形式
        href=href.replace('_m','')
        data_list.append({'title': title,'url': f"https://www.xzmncy.com{href}"})
print(data_list)
#储存数据
df = pd.DataFrame(data_list) #转换为 DataFrame
#写入 Excel 文件
df.to_excel('xzmncy.xlsx', index=False,sheet_name='蚊天帝')
print("数据已保存到 xzmncy.xlsx")

