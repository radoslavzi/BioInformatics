import socket
import socketserver
import threading
from sample_classes import SequenceType
from collections import Counter
import queue
import math

IP = 'localhost'
PORT = 9001
BUFFER_SIZE = 1024
ENCODING = 'ascii'

stream = socket.socket()
stream.connect((IP, PORT))
stream.send(SequenceType.FastQ.name.encode(ENCODING))


def gcContent(data, gcCountList):
    gcCount = data.count("GC")
    gcCountList.append(gcCount)
    return


def addGcCountIfGCIsSplitBetweenChunks(lastChunckEndedWithG, currentChunk, gcCountList):
    if(lastChunckEndedWithG and currentChunk[0] == "C"):
        gcCountList.append(1)

    if(currentChunk.endswith("G")):
        lastChunckEndedWithG = True
    else:
        lastChunckEndedWithG = False
    return lastChunckEndedWithG


def processData(data):
    threads = []
    gcCountList = []
    dataChunkSize = math.ceil(len(data)/10)

    lastChunckEndedWithG = False
    for i in range(0, len(data), dataChunkSize):
        startIndex = i
        endIndex = i+dataChunkSize
        currentChunk = data[startIndex: endIndex]

        lastChunckEndedWithG = addGcCountIfGCIsSplitBetweenChunks(
            lastChunckEndedWithG, currentChunk, gcCountList)

        process_chunks = threading.Thread(
            name="process_chunks",
            target=gcContent,
            args=(currentChunk, gcCountList,)
        )
        process_chunks.start()

        threads.append(process_chunks)

    for t in threads:
        t.join()

    return sum(gcCountList)


def saveContentToFile(data, fileName):
    gc_content_file = open(fileName, 'w')
    gc_content_file.write(data)
    gc_content_file.close()


def receiveData(stream):
    gcCountResult = 0
    while True:
        data = stream.recv(BUFFER_SIZE)
        if not data:
            break
        data = data.decode(ENCODING)

        if(data.endswith('\n')):
            gcCountResult += processData(data.rstrip('\n'))
            saveContentToFile(
                "GC content: " + str(gcCountResult), "data/gc_content.txt")
            stream.close()
            break
        else:
            gcCountResult += processData(data)


process_recieved_data = threading.Thread(
    name="process_recieved_data",
    target=receiveData,
    args=(stream, )
)
process_recieved_data.start()
