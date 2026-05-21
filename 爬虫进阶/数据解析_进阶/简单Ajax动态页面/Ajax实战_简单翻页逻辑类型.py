import asyncio
import json
import aiofiles
import random
import aiohttp
from fake_useragent import UserAgent
import os
"""
目标：爬取目标网址，储存数据为，txt，路径：D:/小说
实现思路：先获取，标题列表然后,再获取章节正文
实现步骤：利用resquests库获取标题，解析Ajax动态渲染的，规律，再构建aiodownload函数异步获取
最后异步保存
"""
async def get_title(session,title_url,headers,title_params):
    """
    获取文章的标题列表
    :param title_url:
    :param headers:
    :return:title_list
    """
    await asyncio.sleep(random.uniform(1, 3))
    async with session.get(title_url, headers=headers, params=title_params) as resp:
        txt_obj = await resp.text()
        js_obj=json.loads(txt_obj)
        title_list = js_obj["list"]
    return title_list
async def aiodownload(session,chapter_url,headers,chapter_params,title,name,sem):
    """
    下载并储存数据
    :param chapter_url:
    :param headers:
    :param chapter_params:
    :return:
    """
    async with sem:  # 控制并发数
        try:
            async with session.get(chapter_url, headers=headers, params=chapter_params) as resp:
                    # 检查状态码
                if resp.status != 200:
                    print(f"请求失败 {chapter_url}，状态码 {resp.status}")
                    return

                    # # 检查内容类型
                    # content_type = resp.headers.get('Content-Type', '')
                    # if 'application/json' not in content_type:
                    #     # 可能是 HTML 错误页面，打印出来调试
                    #     text = await resp.text()
                    #     print(f"返回非 JSON 内容（{content_type}），内容前200字符: {text[:200]}")
                    #     return
                        # 先获取文本内容
                    text = await resp.text() #这里更安全，使用text函数，直接查看源，
                        # 手动解析 JSON
                try:
                    text=await resp.text()
                    data = json.loads(text) #把数据结构转化为，json结构
                    # 正常解析 JSON
                    # data = await resp.json()
                    # 继续处理...
                    content = data.get("txt", "")  #这里用get方法取更安全
                    title= data.get("chaptername","")
                    #数据储存
                    # 创建目录并保存文件
                    folder = rf"D:\小说\{name}"
                    os.makedirs(folder, exist_ok=True)
                    file_path = os.path.join(folder, f"{title}.txt")

                    # 异步写入文件
                    async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
                        await f.write(content)
                    print(f"保存成功{title}")
                except json.JSONDecodeError as e:
                    print(f"JSON 解析失败: {e}, 内容前200字符: {text[:200]}")
                    return

        except asyncio.TimeoutError:
            print(f"请求超时: {chapter_url}")
async def main(title_url,headers,title_params,name):
    #这里创建url
    chapter_url='https://apibi.cc/api/chapter'
    #开始异步
    # 创建共享的 session
    async with aiohttp.ClientSession() as session:
        title_list = await get_title(session, title_url, headers, title_params)
        tasks = []
        sem = asyncio.Semaphore(10)
        for index,title in enumerate(title_list): #对列表添加索引
            chapter_params={'id': '1152',
                        'chapterid': f'{index+1}',}
            tasks.append(aiodownload(session,chapter_url,headers,chapter_params,title,name,sem))
        await asyncio.gather(*tasks)
if __name__ == '__main__':
    name = "九星霸体诀"
    ua = UserAgent()  # 设置ua对象
    headers = {'User-Agent': ua.random}  # 随机选取用户代理
    title_url='https://apibi.cc/api/booklist'
    title_params= {
        'id': '1152',
    }
    asyncio.run(main(title_url,headers,title_params,name))