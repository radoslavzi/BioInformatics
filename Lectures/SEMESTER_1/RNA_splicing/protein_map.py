def ProteinDictDNA():
    	'''Returns a dictionary that translates DNA to Protein.'''
	# Get the raw codon table.
	dna2protein = CodonTableDNA()

	# Convert to dictionary.
	dna_dict = {}
	for translation in dna2protein:
	    dna_dict[translation[0]] = translation[1]

	return dna_dict

def CodonTableDNA():
    	'''Returns a DNA Codon translation list.'''
	table = '''TTT F
	CTT L      
	ATT I      
	GTT V
	TTC F      
	CTC L      
	ATC I      
	GTC V
	TTA L     
	CTA L      
	ATA I      
	GTA V
	TTG L      
	CTG L      
	ATG M      
	GTG V
	TCT S      
	CCT P      
	ACT T      
	GCT A
	TCC S      
	CCC P      
	ACC T      
	GCC A
	TCA S      
	CCA P      
	ACA T      
	GCA A
	TCG S      
	CCG P      
	ACG T      
	GCG A
	TAT Y      
	CAT H      
	AAT N      
	GAT D
	TAC Y      
	CAC H      
	AAC N      
	GAC D
	TAA Stop   
	CAA Q      
	AAA K      
	GAA E
	TAG Stop   
	CAG Q      
	AAG K      
	GAG E
	TGT C      
	CGT R      
	AGT S      
	GGT G
	TGC C      
	CGC R      
	AGC S      
	GGC G
	TGA Stop   
	CGA R      
	AGA R      
	GGA G
	TGG W      
	CGG R      
	AGG R      
	GGG G'''

	table = table.split('\n')
	for index, item in enumerate(table):
		table[index] = item.strip().split()

	return table