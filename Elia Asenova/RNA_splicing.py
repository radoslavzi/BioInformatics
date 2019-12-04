from scripts import ReadFASTA
from protein_map import ProteinDictDNA

dna_list = ReadFASTA('data/rna_splicing.txt')
exon = dna_list[0][1]

for intron in dna_list[1:]:
    # print(intron[1])
    exon = exon.replace(intron[1], '')

# print(exon)

proteinDict = ProteinDictDNA()
# print(proteinDict)


# for index in range(0, len(exon), 3):
#     print(str(exon[index:index+3]))
#     print(proteinDict[exon[index:index+3]])

exon_protein = ''
index = 3
while index < len(exon):
    codon = exon[index:index+3]
    p = proteinDict[codon]
    if p != 'Stop':
        exon_protein += proteinDict[codon]

    index = index + 3

print(exon_protein)