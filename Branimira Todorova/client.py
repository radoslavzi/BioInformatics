import socket
import socketserver
import threading


TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))
#sock.recv(BUFFER_SIZE)

while True:
    data = sock.recv(BUFFER_SIZE)   
    print("Received", data)
 