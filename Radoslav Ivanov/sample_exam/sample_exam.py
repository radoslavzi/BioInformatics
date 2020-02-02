from pathlib import Path

class SequenceBuilder():

    def __init__(self):
        self.sequence = 'ATAGTGGGAAGATTTATA'

    def readFile(self, filePath):
        self.sequence = Path(filePath).read_text()
        return self
    
    def writeInFileReverseOrder(self, filePath):
        with open(filePath, 'w+') as file:
            file.write(self.sequence[::-1])
        
        return self
    
    def writeInFile(self, filePath):
        with open(filePath, 'w+') as file:
            file.write(self.sequence)
        
        return self
    
    def findFrequency(self, character):
        print('%s occurs %d times in sequence' %(character, self.sequence.count(character)))
        return self
    
    def replace(self, replaceDict):
        generatedSeq = ''

        for ch in self.sequence:
            val = replaceDict.get(ch)
            if(not(val is None)):
                generatedSeq += replaceDict.get(ch)
            else:
                generatedSeq += ch

        self.sequence = generatedSeq
        return self
    
    def setSequence(self, seq):
        self.sequence = seq
        return self
    
    def skipFirstLine(self):
        lines = self.sequence.splitlines()[1:]
        self.sequence = ''.join(lines)
        print(self.sequence)
        return self

builder = SequenceBuilder()
builder = builder.findFrequency('A')
builder = builder.readFile('data/sequence_1.seq').writeInFileReverseOrder('reverse_sequence_1.seq')
builder = builder.readFile('data/fasta_seq_1.fa').skipFirstLine().findFrequency('T')
builder = builder.readFile('data/dna_chromosome_1.seq').replace({'A': 'T', 'T': 'A'}).writeInFile('dna_chromosome_solve_1.seq')
builder = builder.readFile('data/dna_chromosome_1.seq').replace({'T': 'U'}).writeInFileReverseOrder('rev_dna_chromosome_1.seq')
