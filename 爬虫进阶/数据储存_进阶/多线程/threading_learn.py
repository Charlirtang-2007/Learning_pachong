import threading #引入线程模块
import time

def worker():
    print("T1 start")
    time.sleep(2)
    print("stop")
def T2():
    print("T2 start")
    print("stop")

def main():
    thread_new1=threading.Thread(target=worker,name="T1")#创建新线程，并以worker函数为目标
    thread_new1.start()#这里启动线程
    thread_new1.join()#等待线程完成
    thread_new2=threading.Thread(target=T2,name="T2")
    thread_new2.start()
    thread_new2.join()
    print("done")
    # print(threading.current_thread().name)#打印当前线程
    # print(threading.active_count())#打印有几个线程
    # print(threading.enumerate()) #打印所有线程


if __name__ == '__main__':#声明
    main()