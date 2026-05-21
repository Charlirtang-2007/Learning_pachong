import asyncio
import aiohttp
"""
目标：抓取目标网址的数据保存为txt
网址："https://www.xzmncy.com/list/57993/",
    "https://www.xzmncy.com/list/56283/",
    "https://www.xzmncy.com/list/57955/"
数据：html源代码
"""
async def aiodownload(url):
    async with aiohttp.ClientSession() as session:#创建对象
        async with session.get(url) as response:#获取响应     #.rsplit("list/",1)[1],从右切list/切一刀，取[1]
            with open(f"{url.rsplit("list/",1)[1].replace("/","")}.txt",'w',encoding="utf-8") as f:
                f.write(await response.text())
async def main():
    url_list=["https://www.xzmncy.com/list/57993/",
              "https://www.xzmncy.com/list/56283/",
              "https://www.xzmncy.com/list/57955/"]
    tasks=[]
    for url in url_list:
        tasks.append(aiodownload(url))
    await asyncio.gather(*tasks)
    print("结束")
if __name__ == '__main__':
    asyncio.run(main())

