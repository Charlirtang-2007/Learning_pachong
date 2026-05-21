import threading
import pprint
import queue
a=[[1,1,1,1,1],[2,2,2,2,2],[3,3,3,3,3],[4,4,4,4,4],[5,5,5,5,5]]
def worker(l,q):
    for i in range(len(l)):
        l[i]=l[i]**2
        # print(l[i])
        # q.put(l)
    q.put(l)
def main():
    q = queue.Queue()#创建队列对象
    threads =[]
    for i in range(5):
        t = threading.Thread(target=worker, args=(a[i],q))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
    results=[]
    for i in range(5):
        results.append(q.get())
    pprint.pprint(results)


if __name__=="__main__":
    main()