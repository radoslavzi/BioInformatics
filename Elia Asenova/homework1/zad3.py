from scripts import countGivenNucleotide

def readFasta(f):
    sequences = []
    dnaSeq = ''
    line = f.readline()
    while line:
        if line.startswith('>'):
            if dnaSeq != '':
                sequences.append(dnaSeq)

            dnaSeq = [line.lstrip('>').rstrip('\n'), '']
        else:
            dnaSeq[1] += line.rstrip('\n')
            
        line = f.readline()
    
    sequences.append(dnaSeq)
    return sequences

def main():
    f = open("data/fasta_seq_1.fa", 'r')
    sequenceList = readFasta(f)
    f.close()

    timinCounterDict = {}
    for dna in sequenceList:
        timinCounterDict[dna[0]] = countGivenNucleotide(dna[1], 'T')

    print(timinCounterDict)

if __name__=="__main__":
    main()