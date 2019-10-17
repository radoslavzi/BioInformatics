class Hamming:
    def __init__(self, seq1, seq2):
        self.seq1 = seq1
        self.seq2 = seq2

    def calculateDistance(self):
        minSeq = self.seq1
        maxSeq = self.seq2

        if(len(self.seq1) > len(self.seq2)):
            minSeq  = self.seq2
            maxSeq = self.seq1

        diff = len(maxSeq) - len(minSeq)

        for i in range(0, len(minSeq)):
            if(minSeq[i] != maxSeq[i]):
                diff += 1

        print(diff)

distance = Hamming('GAGCCTACTAACGGGAT', 'CATCGTAATGACGGCCT')
distance.calculateDistance()
