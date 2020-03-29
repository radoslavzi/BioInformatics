import threading
import time
from queue import Queue 

def read(lock, queue, counter):
    while not queue.empty():
        print(queue.get(counter))
        counter += 1

def write(lock, queue, counter, text, writeCounter):
    for s in text:
        queue.put(s)
    

text = "text"
queue = Queue(len(text))
counter = 0
writeCounter = 0


condition = threading.Condition()

read = threading.Thread(name="read1", target=read, args=(condition, queue,counter))
write = threading.Thread(name="write1", target=write, args=(condition,queue,counter,text,writeCounter))

write.start()
read.start()