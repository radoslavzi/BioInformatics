def main():
    dna_f = open("data/test.txt", 'r')
    sequence = dna_f.readline()
    dna_f.close()

    dic = {'A' : 'T', 'G' : 'C', 'C' : 'G', 'T' : 'A'}
    seq = []
    for i in sequence:
        seq.append(dic.get(i))

    print(",".join(seq))

if __name__ == "__main__":
    main()