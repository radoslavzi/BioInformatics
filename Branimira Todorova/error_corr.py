from scripts import ReadFASTA
from string import maketrans
from collections import Counter

dlist = ReadFASTA('data/corr.txt')

#print(dlist)

def hamingdist(first, second):
    dist = 0
    for i in range(0, len(first)):
        if(first[i] != second[i]):
            dist += 1

    return dist        


def reverseCompl(value):
    intable = 'ATCG'
    outtable = 'TAGC'
    test = maketrans(intable, outtable)
    return value.translate(test)[::-1].lstrip()

seqArray = []
for i in range(0, len(dlist)):
    seqArray.append(dlist[i][1])
    seqArray.append(reverseCompl(dlist[i][1]))

res = {}
var =  Counter(seqArray)
#print(var)
problematic = []
nonprob = []
for i in var:
    print(i)
    if(var[i] == 1):
        problematic.append(i)
    else:
        nonprob.append(i)

print(len(problematic))

#for prob in problematic:
    
#print(len(nonprob))
#reverseCompl()


