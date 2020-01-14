from enum import Enum
from datetime import datetime


class Sequence:
    def __init__(self, content, name):
        self.name = name
        self.content = content

    def parse(self):
        pass


class Fasta_Sequence(Sequence):
    def __init__(self, content, name="", description="", sequence=""):
        super().__init__(content, name)
        self.description = description
        self.sequence = sequence

    def parse(self):
        current = ''
        for line in self.content:
            line = line.rstrip('\n')

            if line[0] == '>':
                current = ''
                first = line[1:]
                if(self.name == ""):
                    self.name = first.split(" ")[0]
                self.description = first.replace(self.name, "")
            else:
                current += line
        self.sequence = current


class Multi_Fasta_Sequence(Sequence):
    def __init__(self, content, name=""):
        super().__init__(content, name)
        self.timestamp = datetime.timestamp(datetime.now())
        self.sequences = []
        currentSequenceLine = []
        name = ''
        for line in self.content:
            if(line[0] == '>'):
                if(len(currentSequenceLine) != 0):
                    fastaSequence = Fasta_Sequence([name] + currentSequenceLine)
                    self.sequences.append(fastaSequence)
                    currentSequenceLine = []

                name = line
            else:
                currentSequenceLine = currentSequenceLine + [line]

        if(len(currentSequenceLine) != 0):
            fastaSequence = Fasta_Sequence([name] + currentSequenceLine)
            self.sequences.append(fastaSequence)

    def parse(self):

        for fasta in self.sequences:
            fasta.parse()


class FastaQ_Sequence(Sequence):

    def __init__(self, content, name="", description="", sequence="", has_quality_value=False, quality_value=""):
        super().__init__(content, name)
        self.description = description
        self.sequence = sequence
        self.has_quality_value = has_quality_value
        self.quality_value = quality_value

    def parse(self):
        splitFirstLine = self.content[0][1:].split(" ")
        if(self.name == ""):
            self.name = splitFirstLine[0]
        self.description = splitFirstLine[1].rstrip('\n')
        self.sequence = self.content[1]
        if(self.content[2][0] == '+'):
            self.has_quality_value = True

        if(self.has_quality_value):
            self.quality_value = self.content[2]


class SequenceType(Enum):
    Fasta = 1
    Multi_Fasta = 2
    FastQ = 3


class SequenceParser:

    def parse(self, seq_type, content, seq_name="not_named"):

        if(seq_type == SequenceType.Fasta):
            return Fasta_Sequence(content, seq_name)
        elif(seq_type == SequenceType.Multi_Fasta):
            return Multi_Fasta_Sequence(content, seq_name)
        elif(seq_type == SequenceType.FastQ):
            return FastaQ_Sequence(content, seq_name)


def main():

    fastaHandle = open("data/fasta.fa", "r")
    fastaLines = fastaHandle.readlines()
    fastaHandle.close()
    fastaSequenceInstance = Fasta_Sequence(fastaLines)
    fastaSequenceInstance.parse()

    multifastaHandle = open('data/multi_fasta.mfa', 'r')
    multifastaLines = multifastaHandle.readlines()
    multifastaHandle.close()
    multifastaSequenceInstance = Multi_Fasta_Sequence(multifastaLines)
    multifastaSequenceInstance.parse()

    fastqHandle = open('data/SRR081241.filt.fastq', 'r')
    fastqLines = fastqHandle.readlines()
    fastqHandle.close()
    fastqSequenceInstance = FastaQ_Sequence(fastqLines)
    fastqSequenceInstance.parse()

    parser = SequenceParser()
    parser.parse(SequenceType.Multi_Fasta, multifastaLines, "multifasta-name")

if __name__ == "__main__":
    main()
