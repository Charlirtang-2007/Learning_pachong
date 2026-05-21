import queue #引入队列库
import requests
import random
import time
import csv
from fake_useragent import UserAgent
import threading #引入线程库
from parsel import Selector
ua = UserAgent() #设置ua对象
headers = {'User-Agent': ua.random}  # 每次随机一个 UA
timeout=(3,5)
start_url='https://www.xzmncy.com/list/56209/'#初始url
url_list=[]#准备一个列表，用来储存url
# 存储结果队列
result_queue = queue.Queue()
#发送请求
response=requests.get(start_url)
#创建一个，Selector对象
selector=Selector(text=response.text)
#提取url并存入列表
hrefs = selector.css('dl dd a::attr(href)').getall()
for href in hrefs:
    url_list.append('https://www.xzmncy.com' + href)

#创建一个队列对象
url_queue = queue.Queue()
#写一个for循环
for url in url_list:
    url_queue.put(url)#将url存入队列
visited = set()#这个集合用来装被访问过的url，方便去重
lock = threading.Lock() #创建一个锁对象
def worker(url_queue): #消费者函数
    """
    定义一个函数，用来取队列url与发送请求和解析数据
    :param url_queue:
    :return:
    """
    while True:
        try:
            url = url_queue.get(timeout=5)
        except queue.Empty:#这里是当抛出空队列异常时停止防止卡死，队列空，退出循环
            break
        #去重
        with lock:
            if url in visited:
                url_queue.task_done() # 标记任务完成
                continue
            visited.add(url)
        #请求和解析
        try:
            # 延迟添加
            delay = random.uniform(1, 3)
            print(f"等待 {delay:.2f} 秒后继续...")
            time.sleep(delay)
            response = requests.get(url=url, headers=headers, timeout=timeout)
            data = response.text
            # 创建selctor对象
            selector = Selector(text=data)
            # 建立一个总对象
            conent = selector.css('div#content')  # 这里不要加extract方法，extract() 会把结果变成 字符串列表，不是选择器对象！
            # 获取标题
            title = selector.css('header h1.title::text').get()  # 用get舒服，不要用extract()
            # print(title)
            # 获取内容                     选择器很简单的，实在不懂，就来问
            content = conent.css('div#text p::text').getall()
            if title and content:
                # 将结果放入结果队列
                result_queue.put({'title': title, 'content': content, 'url': url})
                print(f"[{threading.current_thread().name}] 成功抓取: {title}")
            else:
                print(f"[{threading.current_thread().name}] 页面解析失败: {url}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            url_queue.task_done() #任务标记结束
def result_writer():
    """写入线程：从结果队列取数据，保存到 CSV 文件"""
    with open('chapters.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'url', 'content'])
        writer.writeheader()
        while True:
            try:
                data = result_queue.get(timeout=10)  # 等待 10 秒，如果队列空则认为爬取结束
            except queue.Empty:
                break
            writer.writerow(data)
            result_queue.task_done()
            print(f"已保存: {data['title']}")

def main():
    #创建一个线程列表，用来装已经跑过的线程
    threads=[]
    #创建多线程对象
    for i in range(5): #表示创建5个线程对象
        t = threading.Thread(target=worker, args=(url_queue,))#注意这里是元组，只有一个元素也要记得，加“,”传递队列对象
        t.start() #启动线程
        threads.append(t) #将线程存入列表，方便管理
        #注意不要把for t in threads:
                    #t.join() 放入for循环里面，那样就失去了多线程的意义
    # 4. 启动写入线程
    writer_thread = threading.Thread(target=result_writer, name="Writer")
    writer_thread.start()
    url_queue.join() #这里等待队列清空
    # 通知写入线程结束（通过设置超时，result_writer 会在队列空后退出）
    # 等待写入线程处理完所有结果
    result_queue.join()
    writer_thread.join(timeout=2)
    for t in threads:#写一个for循环用于拿取列表里的线程对象,停止线程
        t.join() #等待所有任务完成
if __name__ == "__main__": #声明
    main()
