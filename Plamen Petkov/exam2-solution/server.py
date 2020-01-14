import socket
import socketserver
import threading
from sample_classes import SequenceType
from sample_classes import SequenceParser

IP = 'localhost'
PORT = 9001
THREAD_POOL = 10
BUFFER_SIZE = 1024
ENCODING = 'ascii'
threads = []

stream = socket.socket()
stream.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
stream.bind((IP, PORT))
stream.listen(THREAD_POOL)
clientConnection, _ = stream.accept()


def processData(clientConnection, data):
    mimeType = ""
    resourceAbsolutePath = ""

    if(data == SequenceType.Fasta.name):
        mimeType = SequenceType.Fasta
        resourceAbsolutePath = 'data/server_fasta.fa'
    elif(data == SequenceType.FastQ.name):
        mimeType = SequenceType.FastQ
        resourceAbsolutePath = 'data/server_fastq.fastq'

    f = open(resourceAbsolutePath, 'r')
    fileContent = f.readlines()
    f.close()

    parcedFile = SequenceParser().parse(mimeType, fileContent).parse()
    clientConnection.send(parcedFile.sequence.encode(ENCODING))


while True:
    clientBufferedRequest = clientConnection.recv(BUFFER_SIZE)
    if not clientBufferedRequest:
        break

    decoded = clientBufferedRequest.decode(ENCODING)
    handle_client_request = threading.Thread(
        name="handle_client_request", target=processData, args=(clientConnection, decoded))
    handle_client_request.start()
    threads.append(handle_client_request)

for t in threads:
    t.join()
