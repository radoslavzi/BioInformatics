from collections import defaultdict

def countGivenNucleotide(sequence, nucleotide):
    counter = 0
    for n in sequence:
        if n == nucleotide:
            counter += 1

    return counter

def main():
    sequence = "ATAGTGGGAAGATTTATA"
    adenineCounter = countGivenNucleotide(sequence, 'A')
    print("Number of Adenine in sequence " + str(adenineCounter))

if __name__ == "__main__":
    main()