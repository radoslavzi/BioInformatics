import socket
import socketserver
import threading
from sequence import SequenceType
from sequence import SequenceParser

TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((TCP_IP, TCP_PORT))
threads = []

sock.listen(5)
conn, addr = sock.accept()

def processData(conn, data):
    typeS = ""
    fileName = ""
    if(data == SequenceType.Fasta.name):
        typeS = SequenceType.Fasta
        fileName = 'data/server_fasta.fa'
    elif(data == SequenceType.FastQ.name):
        typeS = SequenceType.FastQ
        fileName = 'data/server_fastq.fastq'

    print(typeS)
    print(fileName)
    f = open(fileName, 'r')
    output_data = f.readlines()
    f.close()
    parser = SequenceParser()
    test = parser.parse(typeS, output_data, "test")
    test.parse()
    conn.send(test.sequence.encode('ascii'))
    conn.send("XXXXXXXXXXXXX".encode('ascii'))
    #conn.close()

            
while True:
    data = conn.recv(BUFFER_SIZE)
    if not data:
        break
    
    decoded = data.decode('ascii')
    print("Received", decoded)
    newthread = threading.Thread(name="my_thread", target=processData, args=(conn, decoded))
    newthread.start()
    threads.append(newthread)



for t in threads:
    t.join()