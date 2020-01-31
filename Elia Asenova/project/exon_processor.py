import sys, requests, time
from threading import Thread
from queue import Queue
from ensembl_client import EnsemblClient

client = EnsemblClient()

class ExonProcessor():
    def __init__(self, number):
        self.q = Queue(number)

    def getSequence(self, exonId):
        response = client.getRequest("/sequence/id/" + exonId, { "Content-Type" : "text/plain"})
        return response

    def saveResult(self, exon, seq):
        exon["seq"] = seq

    def doWork(self):
        while True:
            exon = self.q.get()
            sequence = self.getSequence(exon["id"].replace(">", ""))
            if sequence.text != "You have exceeded the limit of 15 requests per second; please reduce your concurrent connections":
                self.saveResult(exon, sequence.text)
            else:
                self.q.put(exon)
            time.sleep(1)
            self.q.task_done()   

    def processExons(self, exons): 
        for i in range(20):
            t = Thread(target=self.doWork)
            t.daemon = True
            t.start()

        for exon in exons:
            self.q.put(exon)

        self.q.join()

        return exons