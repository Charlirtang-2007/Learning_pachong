import asyncio
import aiohttp
import requests
from parsel import Selector
import random
import time
import os
import aiofiles
from fake_useragent import UserAgent
"""
目标：爬取整本小说并保存为txt形式
实现思路：利用requests库获取url列表
再利用，异步操作，获取章节正文内容
"""
def get_url(start_url,headers):  #这里直接复制了
    """
    这个函数用来获取并将url装入url_list列表
    :param start_url:初始url
    :return: url_list列表，name小说名字
    """
    #发出请求获取url
    #添加延迟
    delay=random.uniform(1,3)#创建延迟对象
    time.sleep(delay)
    url_list = []#用来储存url的列表
    req = requests.get(start_url, headers=headers,timeout=10)
    #创建选择器
    selector = Selector(text=req.text)
    try:
        id_list = selector.css('div#list dl')
        if id_list:
            for item in id_list:
                hrefs = item.css('dd a::attr(href)').getall()#提取链接
                name = item.css('dt::text').get().replace('章节列表','')#获取本书标题
                for href in  hrefs:
                    url_list.append("https://www.xzmncy.com"+href)
        elif selector.css('ul.chapter'):
            ul_list = selector.css('ul.chapter')
            name=selector.css('header h1.title::text').get()
            for item in ul_list:
                hrefs = item.css('li a::attr(href)').getall()#提取链接
                for  href in hrefs:
                    url_list.append("https://www.xzmncy.com"+href.replace('_m',''))
        else:
            print("请求错误")
    except Exception as e:
        print(e)
    return url_list,name#会以元组的方式返回,并且与顺序有关
async def aiodownload(url, headers, name):
    try:
        # 1. 使用 async with 管理 session
        async with aiohttp.ClientSession() as session:
            # 2. 使用 async with 管理响应
            async with session.get(url, headers=headers, timeout=10) as resp:
                # 3. await 获取 HTML 文本
                html = await resp.text()
                selector = Selector(text=html)

                # 解析标题和正文
                if selector.css('div#htmlContent p::text'):
                    chapter_paragraphs = selector.css('div#htmlContent p::text').getall()
                    title = selector.css('div.bookname h1::text').get()
                elif selector.css('div#content'):
                    chapter_paragraphs = selector.css('div#text p::text').getall()
                    title = selector.css('header h1.title::text').get()
                else:
                    print(f"页面结构不符: {url}")
                    return

                if not title or not chapter_paragraphs:
                    print(f"解析失败: {url}")
                    return

                # 4. 将段落列表合并为字符串
                content = '\n'.join(chapter_paragraphs)

                # 创建目录并保存文件
                folder = rf"D:\小说\{name}"
                os.makedirs(folder, exist_ok=True)
                file_path = os.path.join(folder, f"{title}.txt")

                # 5. 异步写入文件
                async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
                    await f.write(content)
                print(f"保存成功: {title}")

    except asyncio.TimeoutError:
        print(f"请求超时: {url}")
    except Exception as e:
        print(f"未知错误: {e}")
async def main():
    ua = UserAgent()  # 设置ua对象
    headers = {'User-Agent': ua.random}  # 随机选取用户代理
    start_url = "https://www.xzmncy.com/list/56896/"
    url_list,name=get_url(start_url, headers)
    tasks = []
    for url in url_list:
        tasks.append(aiodownload(url,headers,name))
    await asyncio.gather(*tasks)
if "__main__" == __name__:
    t1=time.time()
    asyncio.run(main())
    t2=time.time()
    print(t2-t1)
