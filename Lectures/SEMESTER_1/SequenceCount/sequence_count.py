from collections import defaultdict
from collections import Counter

sequenceString = "AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGC"

class Sequence:
    def __init__(self, seq):
        self.sequence = seq

class SequenceCountService:
    def __init__(self, sequence):
        if not isinstance(sequence, Sequence):
            print("sequence object is not instance of Sequence")
        else:
            self.sequence = sequence
    
    def calculate(self):
        pass

class DefaultDicSequenceCountService(SequenceCountService):
    def calculate(self):
        elementsCount = defaultdict(int)
        sequenceObject = self.sequence
        for c in sequenceObject.sequence:
            elementsCount[c] += 1
        
        print("DefaultDicSequenceCountService count = " + str(elementsCount))

class CounterSequenceCountService(SequenceCountService):
    def calculate(self):
        sequenceObject = self.sequence
        print("CounterSequenceCountService count = " + str(Counter(sequenceObject.sequence)))


def main():
    seqObject = Sequence(sequenceString)
    services = [DefaultDicSequenceCountService(seqObject), CounterSequenceCountService(seqObject)]

    for impl in services:
        impl.calculate()

if __name__ == "__main__":
    main()
