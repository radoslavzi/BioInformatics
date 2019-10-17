import sys

class GC:

    def __init__(self, name):
        self.file_name = name

    def main(self):
        file = open(self.file_name, 'r')
        sequence = {}
        content = file.read().splitlines()
        file.close()

        for line in content:
            if line.startswith('>'):
                key = line
                sequence[key] = ''
            else:
                sequence[key] += line
        
        for key in sequence:
            sequence[key]  = self.calculateGCFrequence(sequence[key])
        
        print(sequence)
    
    def calculateGCFrequence(self, line):
        gcCount = 0

        for val in line:
            if val == 'C' or val == 'G':
                gcCount += 1
        
        return gcCount / len(line)

gc = GC(sys.argv[1])
gc.main()