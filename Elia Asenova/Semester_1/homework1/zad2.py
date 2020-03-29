def reverseStr(str):
    reversed = ""
    for symbol in str:
        reversed = symbol + reversed
    
    return reversed

def main():
    f = open("data/sequence_1.seq", 'r')
    sequence = f.readline()
    f.close()
    
    reversedSequence = reverseStr(sequence)
    
    newFile = open("data/reverse_sequence_1.seq", 'w')
    newFile.write(reversedSequence)
    newFile.close()

if __name__ == "__main__":
    main()