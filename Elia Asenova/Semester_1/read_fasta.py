import sys

def main():
    file_name = sys.argv[1]
    print(file_name)

    f = open(file_name, 'r')
    dict_seq = {}

    for line in f:
        if line.startswith('>'):
            seq_name = line[1:]
            dict_seq[seq_name] = ""
        else:
            current_line = dict_seq.get(seq_name)
            dict_seq[seq_name] = current_line + line
            #print(dict_seq)

    DNA = {}
    for seq in dict_seq:
        sequence = dict_seq[seq]

        G_count = sequence.count('G')
        C_count = sequence.count('C')

        DNA[seq] = (G_count + C_count)*100/len(sequence)
        

    sorted_x = sorted(DNA.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
    print(sorted_x)

if __name__ == "__main__":
    main()