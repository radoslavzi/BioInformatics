from scripts import ReadFASTA

def reverseComplementDNA(acid):
    out = "".maketrans("TAGC", "ATCG")
    return acid.translate(out)[::-1].lstrip()

dna_list = ReadFASTA("data/corr_data.txt")

dna_groups = []
for dna_tuple in dna_list:
    in_group = False
    dna = dna_tuple[1]
    for index, group in enumerate(dna_groups):
        if dna in group or reverseComplementDNA(str(dna)) in group:
            dna_groups[index].append(dna)
            in_group = True
            break
    
    if not in_group:
        dna_groups.append([dna])

dna_groups += [[],[]] + dna_groups

while len(dna_groups) > 2:
    if len(dna_groups[len(dna_groups) - 1]) > 1:
        dna_groups[0].append(dna_groups.pop(len(dna_groups) - 1))
    else:
        dna_groups[1] += dna_groups.pop(len(dna_groups) - 1)




