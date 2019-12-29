import socket
import socketserver
import threading
from sequence import SequenceType

TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))




def processData(sock):

    data = sock.recv(1024)
    if not data:
        return

    if(data == 'XXXXXXXXXXXXX'):
        sock.close()
        return

    data = data.decode('ascii')
    print(data)
    step =  int(len(data)/10) + 1
    res = []
    print(len(data), step)
    for i in range(0, len(data), step):
        #newthread = threading.Thread(name="my_thread", target=calculateGC, args=(data[i: i+step]))
        #newthread.start()
        res.append(data[i: i+step])
    print(res)     


sock.send(SequenceType.Fasta.name.encode('ascii'))

#while True:

    #data = sock.recv(1024)
    #if not data:
    #    break
    
    #if(decoded == 'XXXXXXXXXXXXX'):
    #    sock.close()
    #    break

    #print("Received", decoded)

newthread = threading.Thread(name="my_thread", target=processData, args=(sock, ))
newthread.start()

    #threads.append(newthread)
    #sock.close()



