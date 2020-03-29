def main():
    f = open("data/test.txt", 'r')
    sequence = f.readline()
    f.close()

    seq_rna = sequence.replace("T", "C")
    rna_f = open("data/rna_seq.txt", 'w')
    rna_f.write(seq_rna)
    
    rna_f.close()

if __name__ == "__main__":
    main()