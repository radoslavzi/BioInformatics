from collections import Counter

def task1(seq, charToReturn):
    res = Counter(seq)
    return res[charToReturn]

def reverse(data):
    res = ''
    for item in data[::-1]:
        res += item
    return res

def task2(inFileName, outFileName):
    data = readFile(inFileName)
    writeFile(outFileName, reverse(data))

def processFastaFile(f):
    res = 0
    current = ''
    for line in f:  
        if line[0] == '>':
            res += task1(current, 'T')
            current = ''
        else:
            current += line.rstrip('\n')
    return res

def readFile(inFileName):
    inFile = open(inFileName,'r', buffering=100)
    res = inFile.readline()
    inFile.close()
    return res

def writeFile(outFileName, data):
    outFile = open(outFileName,'a', buffering=100)
    outFile.write(data)
    outFile.close()    

def task3(inFileName):
    inFile = open(inFileName,'r', buffering=100)
    res = processFastaFile(inFile)
    inFile.close()
    return res;


def task4(inFileName, outFileName):
    data = readFile(inFileName)
    data = data.replace('T', 'X')
    data = data.replace('A', 'Y')
    data = data.replace('X', 'A')
    data = data.replace('Y', 'T')
    writeFile(outFileName, data)
    return data

def task5(inFileName):
    data = readFile(inFileName)
    data = data.replace('T', 'U')
    return reverse(data)
    
def main():
    res = task1('ATAGTGGGAAGATTTATA', 'A')
    print("Adenin count : " + str(res))

    task2('data/sequence_1.seq', 'data/reverse_sequence_1.seq')
    res3 = task3('data/fasta_seq_1.fa')
    print("Result for T is " + str(res3))
    task4('data/dna_chromosome_1.seq', 'data/dna_chromosome_solve_1.seq')
    res5 = task5('data/dna_chromosome_1.seq')
    print(res5)

if __name__ == "__main__":
    main()