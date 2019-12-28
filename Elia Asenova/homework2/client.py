import socket
import threading
from scripts import SequenceParser
from scripts import SequenceType
import queue 

TCP_IP = '127.0.0.1'
TCP_PORT = 9001
BUFFER_SIZE = 1024

tcpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsocket.connect((TCP_IP,TCP_PORT))
splitting_threads = []
sum_all = 0
seq_length = 0

class WorkerThread(threading.Thread):
    def __init__(self, args):
        threading.Thread.__init__(self, args=args)
        self.seq = args[0]

    def run(self):
        self.counter = 0
        for n in self.seq:
            if n == 'G' or n == 'C':
                self.counter += 1

    def getCounter(self):
        return self.counter

def splitSequence(seq, out_queue):
    if len(seq) % 10 == 0:
        n = int(len(seq)/10) 
    else:
        n = int(len(seq)/9)
    
    seq_by_parts = [seq[i:i+n] for i in range(0, len(seq), n)]

    counterThreads = []
    for i in seq_by_parts:
        counting_thread = WorkerThread(args=(i,))
        counting_thread.start()
        counterThreads.append(counting_thread)

    for t in counterThreads:
        t.join()

    sum = 0
    for t in counterThreads:
        sum += t.getCounter()

    out_queue.put(sum)

seq_type = SequenceType.FastQ
tcpsocket.send(str(seq_type).encode())

while True:
    data = tcpsocket.recv(BUFFER_SIZE)
    data = data.decode()
    if not data or data == '*':
        break
    result_queue = queue.Queue()
    seq_length += len(data)
    splitting_thread = threading.Thread(name="splitting_thread", target=splitSequence, args=(data, result_queue))
    splitting_thread.start()
    splitting_threads.append(splitting_thread)
    sum_all += result_queue.get()

for t in splitting_threads:
    t.join()

with open("data/gc_content.txt", 'w') as f:
    f.write(str(sum_all/seq_length))

tcpsocket.close()
