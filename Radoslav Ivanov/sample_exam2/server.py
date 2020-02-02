import socket
from sample_exam2 import SequenceType
from sample_exam2 import SequenceParser
from sample_exam2 import _Sequence
import threading

PORT = 9001
LOCAL_SERVER = '127.0.0.1'
BUFFER_SIZE = 1024
THREAD_POOL = 5
ENCODING = 'utf-8'

class ServerBuilder:
    
    def start(self):

 
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((LOCAL_SERVER, PORT))
            s.listen(5)
            clientSocket, addr = s.accept()
            with clientSocket:
                while True:
                    seqType = clientSocket.recv(BUFFER_SIZE)
                    if not seqType:
                        break
                    clientSocket.send(self.sendDataBySeqType(seqType.decode(ENCODING)))
 
    def sendDataBySeqType(self, seqType):
        seq = _Sequence()
        if seqType == SequenceType.Fasta.name:
            seq = SequenceParser().parse(SequenceType.Fasta).readFile('data/server_fasta.fa')
        elif seqType == SequenceType.FastQ.name:
            seq = SequenceParser().parse(SequenceType.FastQ).readFile('data/SRR081241.filt.fastq')
       
        seq.parse()
        return bytes(seq.content, ENCODING)

ServerBuilder().start()