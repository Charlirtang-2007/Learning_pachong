import requests
import threading #线程引入
from parsel import Selector
import queue #引入队列库
import random
import os
import time
from fake_useragent import UserAgent#虚假用户代理
"""
目标：获取网址：https://www.xzmncy.com/list/55737/
的小说标题与正文内容
并储存在txt文件中
"""
def get_url(start_url,headers):
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
            name=selector.css('header h1.title::text').getall()
            for item in ul_list:
                hrefs = item.css('li a::attr(href)').getall()#提取链接
                for  href in hrefs:
                    url_list.append("https://www.xzmncy.com"+href.replace('_m',''))
        else:
            print("请求错误")
    except Exception as e:
        print(e)
    return url_list,name#会以元组的方式返回,并且与顺序有关
def producer(url_list):
    """
    这个函数用来从url_list里面取url装入take_queue队列
    :param url_list: url列表
    :return:take_queue队列
    """
    take_queue = queue.Queue()#建立队列对象
    for url in url_list:
        take_queue.put(url)#把url放入队列
    return take_queue
def consumer(take_queue,headers,result_queue):
    """
    这个函数用来取队列元素与，发送并解析请求
    :param take_queue: take_queue队列
    """
    visited = set()  # 这个集合用来装被访问过的url，方便去重
    lock = threading.Lock()  # 创建一个锁对象
    while True:#无限循环，注意用break语句退出
        try:
            url = take_queue.get(timeout=5)
        except queue.Empty:  # 这里是当抛出空队列异常时停止防止卡死，队列空，退出循环
            break
    #去重
        with lock:#自动化管理
            if url in visited:
                take_queue.task_done()  # 标记任务完成
                continue
            visited.add(url)
        try:#请求与解析
            # 延迟添加
            delay = random.uniform(1, 3)
            print(f"等待 {delay:.2f} 秒后继续...")
            req = requests.get(url, headers=headers,timeout=10)
            selector = Selector(text=req.text)
            try:
                if selector.css('div#htmlContent p::text'):
                    chapter = selector.css('div#htmlContent p::text').getall()
                    title = selector.css('div.bookname h1::text').get()
                elif selector.css('div#content'):
                    chapter = selector.css('div#text p::text').getall()
                    title = selector.css('header h1.title::text').get()
                if title and chapter:
                    # 将结果放入结果队列
                    result_queue.put({"title":title,"chapter":chapter})
                    print(f"[{threading.current_thread().name}] 成功抓取: {title}")
                else:
                    print(f"[{threading.current_thread().name}] 页面解析失败: {url}")
            except Exception as e:
                print(e)
        except Exception as e:
                print(e)
        finally:#完成一个就标记一个
            take_queue.task_done() #任务标记结束
def result_writer(result_queue,book_name):
    """
    写入线程：从结果队列取出数据，保存为单独的文本文件。
    文件保存在当前目录的 name 文件夹下，以标题命名。
    :param result_queue:
    :return:
    """
    # 创建文件夹（如果不存在）
    folder = rf"D:\小说\{book_name}"
    os.makedirs(folder, exist_ok=True)
    while True:
        try:
            # 从队列获取一条数据，最多等待 5 秒
            item = result_queue.get(timeout=5)
        except queue.Empty:
            # 队列空了且超时，认为没有新数据，退出线程
            print("[Writer] 队列已空，写入线程退出")
            break
        title=item.get("title","无")
        chapter=item.get("chapter","无")
        # 写入文件
        file_path = os.path.join(folder, f"{title}.txt")
        try:
            with open(file_path, 'w', encoding='utf-8-sig') as f:
                f.write(f"标题：{title}\n\n")
                for _ in chapter:
                    f.write(_)
            print(f"[Writer] 已保存：{title} -> {file_path}")
        except Exception as e:
            print(f"[Writer] 保存失败 {title}: {e}")

        # 标记该任务已处理完成
        result_queue.task_done()
def main():
    ua = UserAgent()#设置ua对象
    headers = {'User-Agent': ua.random}#随机选取用户代理
    start_url="https://www.xzmncy.com/list/56426/"
    url_list,name=get_url(start_url, headers)
    take_queue=producer(url_list)
    #创建结果队列
    result_queue = queue.Queue()
    #创建线程对象
    threads1=[]
    for i in range(5):
        t1 = threading.Thread(target=consumer,args=(take_queue,headers,result_queue))
        t1.start()
        threads1.append(t1)
        # 启动单个写入线程（传入书名）
    writer_thread = threading.Thread(target=result_writer, args=(result_queue, name))
    writer_thread.start()

    # 等待任务队列清空
    take_queue.join()
    result_queue.join()

    # 等待所有线程结束
    writer_thread.join()
    for t in threads1:
        t.join()
if __name__ == "__main__": #声明
    main()