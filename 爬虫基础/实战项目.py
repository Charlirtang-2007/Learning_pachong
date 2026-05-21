import requests
import random
import parsel #需要安装 pip install parsel
from parsel import Selector
import time
from fake_useragent import UserAgent #可以使用 fake-useragent 库随机生成不同浏览器的 UA
url = "https://www.xzmncy.com/list/56209/26983835.html"#这里设置一个，url对象，方便后续使用
ua = UserAgent() #设置ua对象
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0"}  # 每次随机一个 UA
timeout=(3,5)
#延迟添加
delay = random.uniform(1, 3)
print(f"等待 {delay:.2f} 秒后继续...")
time.sleep(delay)
response = requests.get(url= url,headers=headers,timeout=timeout)
data=response.text
print(data)
#创建selctor对象
selector=Selector(text=data)
#电脑端
chapter=selector.css('div#htmlContent p::text').getall()
name = selector.css('div#read div.current a:nth-child(3)::text').get()#div.current表示，div是父元素，a:nth-child(3)子元素a的第三个
title = selector.css('div.bookname h1::text').get()
print(title)
# #建立一个总对象_手机端
# conent=selector.css('div#content')#这里不要加extract方法，extract() 会把结果变成 字符串列表，不是选择器对象！
# #获取标题
# title=selector.css('header h1.title::text').get()#用get舒服，不要用extract()
# print(title)
# #获取内容                     选择器很简单的，实在不懂，就来问
# chapter=conent.css('div#text p::text').getall()
print(chapter)
# if chapter:  # 确保有内容才写入
#     with open('books.txt', 'a+', encoding='utf-8') as f:
#         f.write(title + '\n')      # 只在开始时写入一次标题
#         for i in chapter:
#             f.write(i + '\n')       # 逐段写入内容
#         f.write('\n')               # 章节结束加个空行
#     print(f"已保存 {len(chapter)} 段内容")
# else:
#     print("未提取到章节内容，请检查CSS选择器")
#实战，最好的的实战就是自己来！！！
#加油，我的朋友