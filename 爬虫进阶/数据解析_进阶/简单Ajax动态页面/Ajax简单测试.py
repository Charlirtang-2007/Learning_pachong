"""
目标：从目标网址获取章节列表
实现思路：抓包分析，找到正确的，请求后，进行基础操作，然后分析，章url之间的关系，然后据此构建url列表
"""
import requests
import json
from fake_useragent import  UserAgent
import random
import time
ua = UserAgent()
headers = {'User-Agent': ua.random}
# book_url='https://dushu.baidu.com/api/pc/getCatalog?data={%22book_id%22:%224306063500%22}'
json_str = '{"book_id":"4306063500"}'
book_url = f'https://dushu.baidu.com/api/pc/getCatalog?data={json_str}'
#发送请求
txt_obj=requests.get(book_url,headers=headers).text
#获取原始响应，解析txt转换成json数据
json_obj=json.loads(txt_obj)
# print(json_obj)#查看原始数据
title_list=json_obj["data"]["novel"]["items"]
# print(title_list)
""""
单章url
chapter_data='{"book_id":"4306063500","cid":"4306063500|1569782244","need_bookinfo":1}'
chapter_url=f'https://dushu.baidu.com/api/pc/getChapterContent?data={chapter_data}'
下一章
chapter_data='{"book_id":"4306063500","cid":"4306063500|1569782245","need_bookinfo":1}'
chapter_url=f'https://dushu.baidu.com/api/pc/getChapterContent?data={chapter_data}'
只有cid在变
"""
# print(title_list)
chapter_urls=[]
for i in title_list:
    title=i["title"]
    cid=i["cid"]
    # print(cid)
#开始构建url列表
    chapter_data = '{"book_id":"4306063500","cid":"4306063500|'+f'{cid}'+'","need_bookinfo":1}' #这里用拼接
    chapter_url=f'https://dushu.baidu.com/api/pc/getChapterContent?data={chapter_data}'
    chapter_urls.append((title, chapter_url))#这里传元组
print(f'共获取到{len(chapter_urls)}章')
for idx, (title, url) in enumerate(chapter_urls[:3], 1):
    print(f"正在抓取第{idx}章：{title}")
    try:
        resp = requests.get(url, headers=headers)
        content_data = resp.json()
        content = content_data["data"]["novel"]["content"]  # 注意：实际字段名可能需要调整
        # 保存到文件
        with open(f"{title}.txt", "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  保存成功")
        time.sleep(random.uniform(0.5, 1.5))  # 礼貌爬取
    except Exception as e:
        print(f"  抓取失败：{e}")








