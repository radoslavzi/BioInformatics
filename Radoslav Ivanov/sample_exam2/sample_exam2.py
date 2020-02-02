from pathlib import Path
from time import time
import enum

class _Sequence():
    def __init__(self, name = '', content = ''):
        self.name = name
        self.content = content
    
    def readFile(self, filePath):
        self.fileContentLines = Path(filePath).read_text().splitlines()
        return self
    
    def parse(self):
        pass

class Fasta_Sequence(_Sequence):

    def getFirstLine(self):
        return self.fileContentLines[0]
        
    def getSequence(self):
        return ''.join(self.fileContentLines[1:])
    
    def parse(self):
        self.name = self.getFirstLine()
        self.content = self.getSequence()

class Multi_Fasta_Sequence(_Sequence):

    def constructName(self, line):
        idx = line.find(' ')
        return line[0:idx] + ' ' + str(time())
    
    def addFastaSequence(self, name, content):
        self.multiFastaFormats.append(Fasta_Sequence(name, content))
    
    def parseIntoMultipleFastaFormats(self):
        self.currentName = ''
        self.currentSeq = ''

        for line in self.fileContentLines:
            if line.startswith('>'):
                self.addFastaSequence(self.currentName, self.currentSeq)
                self.currentName = self.constructName(line)
                self.currentSeq = ''
            else:
                self.currentSeq += line

    def parse(self):
        self.multiFastaFormats = list()
        self.parseIntoMultipleFastaFormats()

class Fasta_Q_Sequence(_Sequence):
    def getFirstLine(self):
        return self.fileContentLines[0]
        
    def getSequence(self):
        return ''.join(self.fileContentLines[1])
    
    def isQualityChecked(self):
        return self.fileContentLines[2].startswith('+')
    
    def getQualityValue(self, hasQualityValue):
        if hasQualityValue:
            return self.fileContentLines[3]
        return ''
    
    def parse(self):
        self.name = self.getFirstLine()
        self.content = self.getSequence()
        self.hasQualityValue = self.isQualityChecked()
        self.qualityValue = self.getQualityValue(self.hasQualityValue)

class SequenceType(enum.Enum):
    Fasta = 1
    Multi_Fasta = 2
    FastQ = 3

class SequenceParser:

    def parse(self, seq_type, content = '', name = ''):

        if(seq_type == SequenceType.Fasta):
            return Fasta_Sequence(content, name)
        elif(seq_type == SequenceType.Multi_Fasta):
            return Multi_Fasta_Sequence(content, name)
        elif(seq_type == SequenceType.FastQ):
            return Fasta_Q_Sequence(content, name)

        
seq = SequenceParser().parse(SequenceType.FastQ).readFile('data/SRR081241.filt.fastq').parse()
seq = SequenceParser().parse(SequenceType.Multi_Fasta).readFile('data/multi_fasta.mfa').parse()
seq = SequenceParser().parse(SequenceType.Fasta).readFile('data/fasta.fa').parse()