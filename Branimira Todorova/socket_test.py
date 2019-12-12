import socket
import socketserver
import threading


TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024


tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

def readingFile(conn, ip,port):
    
    file = open('test.txt', 'rb')
    while True:
        data = file.read(BUFFER_SIZE)
        if not data:
            file.close()
            #conn.close()
            break 
        else:
            print(data)
            conn.send(data)


while True:
    tcpsock.listen(5)
    print("Waiting for incoming connections...")
    (conn, (ip,port)) = tcpsock.accept()
    print('Got connection from ', (ip,port))
    newthread = threading.Thread(name="my_thread", target=readingFile, args=(conn, ip,port,))
    newthread.start()
    threads.append(newthread)


for t in threads:
    t.join()