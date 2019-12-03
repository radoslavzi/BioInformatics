def main():
    f = open("data/dna_chromosome_1.seq", 'r')
    sequence = f.readline()
    f.close()

    sequence = sequence.rstrip('\n')
    sequence = sequence.replace('A','S')
    sequence = sequence.replace('T', 'A')
    sequence = sequence.replace('S', 'T')
    
    modifiedSeq = sequence
    modifiedSeqFile = open("data/dna_chromosome_solve_1.seq", 'w')
    modifiedSeqFile.write(modifiedSeq)
    modifiedSeqFile.close()

if __name__ == "__main__":
    main()