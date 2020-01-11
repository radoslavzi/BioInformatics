import socket
import socketserver
import threading
from sequence import SequenceType
from collections import Counter
import queue

TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))

def calculateGC(data, que):
    res = Counter(data)
    que.put(res['G'] + res['C'])
    return res['G'] + res['C']


def processData(data):

    step =  int(len(data)/10) + 1
    threads = []
    que = queue.Queue()
    for i in range(0, len(data), step):
        newthread = threading.Thread(name="my_thread", target=calculateGC, args=(data[i: i+step],que,))
        newthread.start()
        threads.append(newthread)

    for t in threads:
        t.join() 

    saveGCContent(que, len(data))    


def saveGCContent(que, length):
    result = 0
    while not que.empty():
        result += que.get()

    gc_content_file = open("data/gc_content.txt", 'w')
    gc_content_file.write("The GC content is " + str(result/length))
    gc_content_file.close()


sock.send(SequenceType.FastQ.name.encode('ascii'))


def receiveData(sock):

    while True:
        data = sock.recv(BUFFER_SIZE)
        if not data:
            break
        data = data.decode('ascii')

        if(data.endswith('XXXXXXXXXXXXX')):
            processData(data.rstrip('XXXXXXXXXXXXX'))
            sock.close()
            break
        else:
            processData(data)

        

newthread = threading.Thread(name="my_thread", target=receiveData, args=(sock, ))
newthread.start()





