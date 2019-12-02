import threading
import time
import logging
import queue

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s (%(threadName)-2s) %(message)s',)

def worker(lock, queue):
    logging.debug(threading.currentThread().getName())

    for i in range(10):
        q.put(threading.currentThread().getName() + " " + str(i))

    with lock:
        lock.notifyAll()

    print(threading.currentThread().getName(), "Finish")
 

def service(lock, queue):
     print(threading.currentThread().getName(), "Waiting")    

     with lock:
         lock.wait()
     while(not queue.empty()):
        print(threading.currentThread().getName(), "Done item " + queue.get())       
       

condition = threading.Condition()

condition
q = queue.Queue()

    

w1 = threading.Thread(name="worker1", target=worker, args=(condition,q))
w2 = threading.Thread(name="worker2", target=worker, args=(condition,q))
s1 = threading.Thread(name="service", target=service,  args=(condition,q))

s1.start()
time.sleep(2)
w1.start()
w2.start()


print("end")