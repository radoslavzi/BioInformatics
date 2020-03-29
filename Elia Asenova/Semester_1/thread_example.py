import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s (%(threadName)-2s) %(message)s',)

def worker(lock):
    logging.debug("WORK")
    time.sleep(10)
    print(threading.currentThread().getName(), "FINISH")
    with lock:
        lock.notify()

def service(lock):
    print(threading.currentThread().getName(), "Waiting")
    with lock:
        lock.wait()
    print(threading.currentThread().getName(), "DONE")

condition = threading.Condition()

w1 = threading.Thread(name="my_thread1", target=worker, args=(condition,), daemon=True)
w2 = threading.Thread(name="my_thread2", target=worker, args=(condition,), daemon=True)

s1 = threading.Thread(name="service", target=service, args=(condition,),daemon=True)

w1.start()
w2.start()
s1.start()

for thread in threading.enumerate():
    logging.debug(thread.getName())