from scripts import ReadFASTA
# from string import maketrans

def reverseComplementDNA(dna):
    intable = "ATGC"
    outtable = "TACG"
    out = "".maketrans(intable, outtable)
    return dna.translate(out)

dna_list = ReadFASTA('data/corr.txt')
dna_dict = {}

for dna in dna_list[1:]: 
    dna_dict[dna[1]] = 0

dna_groups = []
for dna_tuple in dna_list:
    in_group = False
    dna = dna_tuple[1]
    complementDNA = reverseComplementDNA(dna[1])
    for index, group in enumerate(dna_groups):
        if in_group


print(dna_dict)



print(reverseComplementDNA("AGGGGGA"))


