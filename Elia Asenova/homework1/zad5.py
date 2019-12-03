from scripts import reverseStr

def main():
    dnaFile = open("data/dna_chromosome_1.seq", 'r')
    dnaSequence = dnaFile.readline()
    dnaFile.close()

    rnaSequence = dnaSequence.replace('T', 'U')
    reversedRnaSequence = reverseStr(rnaSequence)

    rnaFile = open("data/rna_chromosome_1.seq", 'w')
    rnaFile.write(reversedRnaSequence)
    rnaFile.close()

if __name__ == "__main__":
    main()