from collections import defaultdict
from collections import Counter

sequence = "AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGC"

class Sequence:
    def __init__(self, seq):
        self.sequence = seq

class SequenceCountService:
    def __init__(self, sequence):
        if not isinstance(sequence, Sequence):
            exit()
            print("sequence object is not instance of Sequence")
        else:
            self.sequence = sequence


    def calculate(self):
        pass

str(SequenceCountService.calculate)

class DeafultDictSequenceCountService(SequenceCountService):
    def calculate(self):
        elementsCount = defaultdict(int)
        sequenceObject = self.sequence
        for c in sequenceObject:
            elementsCount[c] += 1

        print("DeafultDictSequenceCountService count = " + str(elementsCount))


service = DeafultDictSequenceCountService(Sequence(sequence))
service.calculate()

def main():
    countElements = {}

    for c in sequence:
        if not countElements.get(c):
            countElements[c] = 1
        else:
            countElements[c] += 1

    print("countElements = " + str(countElements))

    defDicCount = defaultdict(int)
    for c in sequence:
        defDicCount[c] += 1

    print("defDicCount = " + str(defDicCount))

    print(Counter(sequence))
        
if __name__ == "__main__":
    main()