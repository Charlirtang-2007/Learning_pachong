import json
import requests
import random
from parsel import Selector
import time
from fake_useragent import UserAgent #可以使用 fake-useragent 库随机生成不同浏览器的 UA
url = "https://www.xzmncy.com/list/55501/"#这里设置一个，url对象，方便后续使用
ua = UserAgent() #设置ua对象
headers = {'User-Agent': ua.random}  # 每次随机一个 UA
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
#                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
timeout=(3,5)
#延迟添加
delay = random.uniform(1, 3)
print(f"等待 {delay:.2f} 秒后继续...")
time.sleep(delay)
#发送请求
response = requests.get(url, headers=headers, timeout=timeout)
print(response.text)
#解析数据
selector = Selector(text=response.text)
data_list=[]
try:
    id_list=selector.css('div#list dl')
    if id_list:
        for item in id_list:
            hrefs = item.css('dd a::attr(href)').getall()
            titles = item.css('dd a::text').getall()
            for title,href in zip(titles,hrefs):
                data_dict = {}
                data_dict[title]=href
                data_list.append(data_dict)
    elif selector.css('ul.chapter'):
        ul_list = selector.css('ul.chapter')
        for item in ul_list:
            hrefs = item.css('li a::attr(href)').getall()
            titles = item.css('li a::text').getall()
            for title,href in zip(titles,hrefs):
                data_dict = {}
                href = href.replace('_m', '')
                data_dict[title]=href#这是字典对像
                data_list.append(data_dict) #这样就是数组对象了
    else:
        print("请求错误")
except Exception as e:
    print(e)
print(data_list)
# #数据储存
# with open('xzmncy.json', 'w', encoding='utf-8') as f:
#     json.dump(data_list, f, indent=2, ensure_ascii=False)