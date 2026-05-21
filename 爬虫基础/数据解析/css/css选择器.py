import requests
import random
import parsel #需要安装 pip install parsel
from parsel import Selector
import time
from fake_useragent import UserAgent #可以使用 fake-useragent 库随机生成不同浏览器的 UA
url = "https://www.xzmncy.com/list/56209/26983835.html"#这里设置一个，url对象，方便后续使用
ua = UserAgent() #设置ua对象
headers = {'User-Agent': ua.random}  # 每次随机一个 UA
timeout=(3,5)
#延迟添加
delay = random.uniform(1, 3)
print(f"等待 {delay:.2f} 秒后继续...")
time.sleep(delay)
response = requests.get(url= url,headers=headers,timeout=timeout)
data=response.text
# print(data)
#创建selctor对象
selector=Selector(text=data)
#建立一个总对象
conent=selector.css('div.readbar')#这里不要加extract方法，extract() 会把结果变成 字符串列表，不是选择器对象！
#获取标题
title=conent.css('div.bookname h1::text').get()#用get舒服，不要用extract()
print(title)
#获取内容                     选择器很简单的，实在不懂，就来问
chapter=conent.css('div#htmlContent p::text').getall()
for i in chapter:#简单for循环
    print(i)

