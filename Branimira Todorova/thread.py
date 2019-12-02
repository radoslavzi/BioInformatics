import threading
import time
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s (%(threadName)-2s) %(message)s',)

def worker(lock):
    logging.debug(threading.currentThread().getName())
    #print(threading.currentThread().getName(), "work")
    time.sleep(5)
    print(threading.currentThread().getName(), "Finish")
    with lock:
        lock.notify()
 

def service(lock):
     print(threading.currentThread().getName(), "Waiting for")    
     with lock:
         lock.wait()
     print(threading.currentThread().getName(), "done")       


condition = threading.Condition()
w1 = threading.Thread(name="my_thread", target=worker, args=(condition,))
w2 = threading.Thread(name="my_thread", target=worker, args=(condition,))

s1 = threading.Thread(name="my_thread2", target=service,  args=(condition,))


w1.start()
w2.start()
s1.start()

for thread in threading.enumerate():
    logging.debug(thread.getName())
