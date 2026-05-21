import asyncio #引入asyncio模块
import time

# async def func1():#加上async修饰，输出多协程对象
#     print("h")
#     # time.sleep(1) #同步操作改异步
#     await asyncio.sleep(1)
#     print("w")
# async def func2():
#     print("he")
#     # time.sleep(1)
#     await asyncio.sleep(1)
#     print("wo")
# async def func3():
#     print("hel")
#     # time.sleep(1)
#     await asyncio.sleep(1)
#     print("wor")
# async def func4():
#     print("hell")
#     # time.sleep(1)
#     await asyncio.sleep(1)
#     print("worl")
# async def func5():
#     print("hello")
#     # time.sleep(1)
#     await asyncio.sleep(1)
#     print("world")
# async def main():
#     # 并发执行所有协程，等待全部完成
#     # await asyncio.gather(func1(), func2(), func3(), func4(), func5())
#     tasks=[func1(),func2(),func3(),func4(),func5()]
#     await asyncio.gather(*tasks)#解包后可以传入
#
# if __name__ == "__main__":
#     t1 = time.time()
#     asyncio.run(main())
#     t2 = time.time()
#     print(t2 - t1)

#模拟爬虫流程
async def download(url):#这里写一个，下载函数模拟，get_url函数
    print("开始执行")
    await asyncio.sleep(3)
    print(url+"执行完成")
async def main():
    url_list=[
        "www.baidu.com",
        "www.qq.com",
        "www.sinaiping.com",
        "www.163.com"
    ]
    tasks=[]
    for url in url_list:#for循环
        d=download(url)#创建对象
        tasks.append(d)
    await asyncio.gather(*tasks)
if __name__ == '__main__':
    t1 = time.time()
    asyncio.run(main())
    t2 = time.time()
    print(t2 - t1)
