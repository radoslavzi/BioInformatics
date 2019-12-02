from collections import defaultdict
from collections import Counter

seq = "AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGC"
#print(len(seq))
class Sequence:
    def __init__(self, seq):
        self.seq = seq

    def calc(self):
        pass

seq2 = Sequence(seq)

class SequenceCountService:
    def __init__(self, sequence):
        if not isinstance(sequence, Sequence):
            print('Error')
        else:      
            self.sequence = sequence
    def calc(self):
        pass    

class DefSequenceCountService(SequenceCountService):

    def calc(self):
        defDic = defaultdict(int)
        for c in self.sequence.seq:
            defDic[c] += 1
        print(defDic)

class CounterSequenceCountService(SequenceCountService):

    def calc(self):
        print(Counter(self.sequence.seq))


def main():
    service = DefSequenceCountService(seq2)
    service.calc()

    service2 = CounterSequenceCountService(seq2)
    service2.calc()

    arr = [service, service2]
    for tt in arr:
        tt.calc()


def main1():
    print(seq)
    countElem = {}


    for c in seq:
        if not countElem.get(c):
            countElem[c] = 1
        else:
            countElem[c] += 1 


    print(countElem)     
    defDic = defaultdict(int)
    for c in seq:
        defDic[c] += 1

    print(defDic)
    
    print(Counter(seq))

if __name__ == "__main__":
    main()