
import random
import time
from collections import Counter
import operator

def main1():
    switcher = { 0 : 'A', 1 : 'C', 2 : 'T', 3 : 'G'}

    file = open("test.txt",'a', buffering=100)
    for i in range(1, 10000):
        symbol =  random.choice(switcher)
        file.write(symbol)
        #time.sleep(0.2)
    file.close()    

def main2():
 

    file = open("test.txt",'r', buffering=100)
   
    data = file.readline()
    file.close()
    #comp_seq = data.replace("G", "X")
    #comp_seq = comp_seq.replace("C", "G")
    #comp_seq = data.replace("X", "C")
    #comp_seq = comp_seq1.replace("A", "T")
    #comp_seq = comp_seq2.replace("T", "A")
    dic = { 'A' : 'T', 'G' : 'C', 'C' : 'G', 'T' : 'A'}
    seq = []
    for i in data:
        seq.append(dic.get(i))
        
    comp_seq_file = open("comp_seq_file.txt", 'w')
    comp_seq_file.write("".join(seq))
    comp_seq_file.close()


def main():
    f =  open("test2.txt",'r')
    dic_seq = {}
    for line in f:
        if line.startswith(">"):
            seq_name = line[1:]
            dic_seq[seq_name] = ""
        else:
            print(seq_name)
            curLine = dic_seq.get(seq_name)
            dic_seq[seq_name] = curLine + line
            print(dic_seq[seq_name])   
            
    DNA = {}
    for i in dic_seq:
        seq = dic_seq.get(i)
        valueG = seq.count('G')
        valueC = seq.count('C')
        DNA[i]  = (valueG + valueC)*100/len(seq)

    test = sorted(DNA.items(), key=operator.itemgetter(1), reverse=True)
    print(test)
   # print(Counter(dic_seq[]))
    
if __name__ == "__main__":
    main()

