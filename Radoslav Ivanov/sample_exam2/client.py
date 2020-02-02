import socket
from sample_exam2 import SequenceType
import threading
import math
from pathlib import Path

PORT = 9001
LOCAL_SERVER = '127.0.0.1'
BUFFER_SIZE = 1024
ENCODING = 'utf-8'

class ClientBuilder:

    def start(self):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as stream:
            stream.connect((LOCAL_SERVER, PORT))
            self.sendData(SequenceType.Fasta.name, stream)
            gcCount =  self.recvData(stream) # threading.Thread(target=, args=(s,), daemon=True)
            self.writeIntoFile(gcCount, 'gc_content.txt')
    
    def sendData(self, text, sock):
        sock.sendall(bytes(text, ENCODING))
    
    def recvData(self, sock):
        data =  sock.recv(BUFFER_SIZE).decode(ENCODING)
        dataChunkSize = math.ceil(len(data)/10)
        numList = list()

        for idx in range(0, len(data), dataChunkSize):
            parseData = data[idx: idx + dataChunkSize]
            thread = threading.Thread(target=self.calculateGCCount, args=(parseData, numList, ), daemon=True)
            thread.start()
            thread.join()
        print(data)
        return sum(numList)
    
    def writeIntoFile(self, count, filePath):
        with open(filePath, 'w+') as file:
            file.write('GC count %d' %count)

    def calculateGCCount(self, data, numList):
        numList.append(data.count('G') + data.count('C'))

ClientBuilder().start()