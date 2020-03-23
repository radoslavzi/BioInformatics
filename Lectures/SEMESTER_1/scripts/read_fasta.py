def ReadFASTA(data_location):
    if data_location[-4:] == '.txt':
        with open(data_location, 'r') as f:
            return ParseFASTA(f)


def ParseFASTA(f):
    fasta_list = []
    current_dna = ''
    for line in f:
        if line[0] == '>':
            try:
                if current_dna != '':
                    fasta_list.append(current_dna)
            except UnboundLocalError:
                pass
            current_dna = [line.lstrip('>').rstrip('\n'), '']
        else:
            current_dna[1] += line.rstrip('\n')

    fasta_list.append(current_dna)

    return fasta_list
