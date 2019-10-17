class Motif:
    def __init__(self, dna, pattern):
        self.dna = dna
        self.pattern = pattern
    
    def calculateOccurrance(self):
        counter = 0
        while(counter < len(self.dna)):
            patternCounter = 0
            innerCounter = counter
            while(innerCounter < len(self.dna) and 
                 patternCounter < len(self.pattern) and
                 self.dna[innerCounter] == self.pattern[patternCounter]):
                patternCounter+=1
                innerCounter+=1

            if(patternCounter >= len(self.pattern)):
                print(innerCounter - patternCounter + 1)

            counter += 1
            


m = Motif('GATATATGCATATACTT', 'ATAT')
m.calculateOccurrance()