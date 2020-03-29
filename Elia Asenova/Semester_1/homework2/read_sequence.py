from collections import defaultdict
from datetime import datetime
from enum import Enum

class _Sequence:
    def __init__(self, name, content):
        self.name = name
        self.content = content

    def parse(self):
        pass

class Fasta_Sequence(_Sequence):
    def parse(self):
        dnaSeq = []
        description = ''
        sequence = ''
        content = self.content
        for line in content.splitlines():
            if line.startswith('>'):
                description = line.lstrip('>').rstrip('\n')
            else:
                sequence += line.rstrip('\n')

        dnaSeq.append(description)
        dnaSeq.append(sequence)

        return dnaSeq

class Multi_Fasta_Sequence(_Sequence):
    def parse(self):
        sequences = defaultdict(Fasta_Sequence)
        dnaSeq = ''
        content = self.content
        for line in content.splitlines():
            timestamp = str(datetime.timestamp(datetime.now()))
            if line.startswith('>'):
                if dnaSeq != '':
                    sequences[dnaSeq[0] + ' ' + timestamp] = dnaSeq[1]
                
                dnaSeq = [line.lstrip('>').rsplit(' ')[0], '']
            else:
                dnaSeq[1] += line.rstrip('\n')
    
        sequences[dnaSeq[0] + ' ' + timestamp] = dnaSeq[1]

        return sequences

class FastaQ_Sequence(_Sequence):
    def parse(self):
        dnaSeq = []
        description = ''
        sequence = ''
        has_quality_value = False
        content = self.content
        for line in content.splitlines():
            if line.startswith('@'):
                description = line.lstrip('@').rstrip('\n')
            elif line.startswith('+'):
                has_quality_value = True
            elif has_quality_value == True:
                quality_value = line
            else:    
                sequence += line.rstrip('\n')

        dnaSeq.append(description)
        dnaSeq.append(sequence)
        dnaSeq.append(has_quality_value)
        if quality_value:
            dnaSeq.append(quality_value)

        return dnaSeq

class SequenceType(Enum):
    Fasta = 1
    Multi_Fasta = 2
    FastQ = 3

class SequenceParser:
    def parse(self, seq_type, seq_name, content):
        seq = ''
        if seq_type == SequenceType.Fasta:
            seq = Fasta_Sequence(seq_name, content)
            seq = seq.parse()
        elif seq_type == SequenceType.Multi_Fasta:
            seq = Multi_Fasta_Sequence(seq_name, content)
            seq = seq.parse()
        elif seq_type == SequenceType.FastQ:
            seq = FastaQ_Sequence(seq_name, content)
            seq = seq.parse()
        
        return seq

def main():
    seq_parser = SequenceParser()
    with open("data/fasta.fa", 'r') as f:
        fasta_data = f.read()
    fasta_sequence = seq_parser.parse(SequenceType.Fasta, "fasta", fasta_data)
    print(fasta_sequence)

    with open("data/multi_fasta.mfa", 'r') as f:
        multifasta_data = f.read()
    multifasta_sequences = seq_parser.parse(SequenceType.Multi_Fasta, "multi_fasta", multifasta_data)
    print(multifasta_sequences)

    with open("data/SRR081241.filt.fastq", 'r') as f:
        fastq_data = f.read()
    fastq_sequence = seq_parser.parse(SequenceType.FastQ, "fastq", fastq_data)
    print(fastq_sequence)

if __name__ == "__main__":
    main()