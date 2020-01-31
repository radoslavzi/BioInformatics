import queue
import threading

class WorkerThread(threading.Thread):
    def __init__(self, args):
        threading.Thread.__init__(self, args=args)
        self.seq = args[0]

    def run(self):
        self.counter = 0
        for n in self.seq:
            if n == 'G' or n == 'C':
                self.counter += 1

    def getCounter(self):
        return self.counter

def splitSequence(seq, out_queue):
    if len(seq) % 10 == 0:
        n = int(len(seq)/10) 
    else:
        n = int(len(seq)/9)
    
    seq_by_parts = [seq[i:i+n] for i in range(0, len(seq), n)]

    counterThreads = []
    for i in seq_by_parts:
        counting_thread = WorkerThread(args=(i,))
        counting_thread.start()
        counterThreads.append(counting_thread)

    for t in counterThreads:
        t.join()

    sum = 0
    for t in counterThreads:
        sum += t.getCounter()

    out_queue.put(sum)

def processGCContent(seq):
    splitting_threads = []
    sum_all = 0
    seq_length = 0

    result_queue = queue.Queue()
    seq_length += len(seq)
    splitting_thread = threading.Thread(name="splitting_thread", target=splitSequence, args=(seq, result_queue))
    splitting_thread.start()
    splitting_threads.append(splitting_thread)
    sum_all += result_queue.get()

    for t in splitting_threads:
        t.join()

    return round(sum_all/seq_length*100, 2)

def swapNucleotides(seq, n1, n2):
    seq = seq.replace(n1,'S')
    seq = seq.replace(n2, n1)
    seq = seq.replace('S', n2)
    
    return seq