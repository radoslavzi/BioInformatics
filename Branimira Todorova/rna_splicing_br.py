from scripts import ReadFASTA
from protein_map import ProteinDictDNA


dlist = ReadFASTA('data/rosalind_splc.txt')
#print(dlist)

RNA = dlist[0][1]

lenDNA = len(dlist)

for i in range(1, lenDNA):
    RNA = RNA.replace(dlist[i][1], '')

#print(RNA)   

prot_dct = ProteinDictDNA()

protein = ''
for i in range(0, len(RNA), 3):
    test = RNA[i: i+3]
    if(prot_dct[test] != 'Stop'):
        protein += prot_dct[test]

print(protein)