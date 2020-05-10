# Consumer Producer
import threading
import time
import logging
import queue

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s (%(threadName)-2s)) %(message)s',)

def feed(lock, elements, q1):
    logging.debug("Feeding %s", threading.currentThread().getName())
    for e in elements:
        q1.put(e)

def consume(lock, queue):
    logging.debug("Hello consume")
    while not q1.empty():
        logging.info("Getting element %s", q1.get())


q1 = queue.Queue()

condition = threading.Condition()

f2 = threading.Thread(name="feed_2", target=feed, args=(condition,[6,7,8,9,10],q1))
f1 = threading.Thread(name="feed_1", target=feed, args=(condition,[1,2,3,11,4,5],q1))
c1 = threading.Thread(name="consume_2", target=consume, args=(condition,q1))

f1.start()
f2.start()
c1.start()
