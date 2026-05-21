from threading import Thread
import threading
def worker1():
    global A,lock
    lock.acquire()
    for i in range(5):
        A+=1
        print("worker1 A:",A)
    lock.release()
def worker2():
    global A,lock
    with lock: #with 更高效
        for i in range(5):
            A+=5
            print("worker2 A:",A)
def main():
    thread1 = threading.Thread(target=worker1)
    thread2 = threading.Thread(target=worker2)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
if __name__=='__main__':
    lock = threading.Lock()
    A = 0  # 全局变量
    main()