from enum import Enum
from datetime import datetime

class Sequence:
    def __init__(self, content, name):
        self.name = name
        self.content = content

    def parse(self):
        pass    



class Fasta_Sequence(Sequence):

    def __init__(self, content, name="", description="", sequence=""):
        super().__init__(content, name)
        self.description = description
        self.sequence = sequence
 

    def parse(self):
        current = ''
        for line in self.content:  
            line = line.rstrip('\n')
            
            if line[0] == '>':
                current = ''
                first = line[1:]
                if(self.name == ""):
                    self.name = first.split(" ")[0]
                self.description = first.replace(self.name, "")
            else:
                current += line
        self.sequence = current
    
class Multi_Fasta_Sequence(Sequence):

    def __init__(self, content, name=""):
        super().__init__(content, name)
        self.timestamp = datetime.timestamp(datetime.now())
        self.fastas = []
        current = []
        name = ''
        for line in self.content:  
            if(line[0] == '>'):
                if(len(current) != 0):                    
                    fasta = Fasta_Sequence([name] + current)
                    self.fastas.append(fasta) 
                    current = []

                name = line                           
            else:
                current = current + [line]

        if(len(current) != 0):  
            fasta = Fasta_Sequence([name] + current)
            self.fastas.append(fasta)  
    

    def parse(self):

        for fasta in self.fastas:
            fasta.parse()

                      
class FastaQ_Sequence(Sequence):

    def __init__(self, content, name="", description="", sequence="", has_quality_value=False, quality_value=""):
        super().__init__(content, name)
        self.description = description
        self.sequence = sequence
        self.has_quality_value = has_quality_value
        self.quality_value = quality_value


    def parse(self):
        temp = self.content[0][1:].split(" ")
        if(self.name == ""):
            self.name = temp[0]
        self.description =  temp[1].rstrip('\n')
        self.sequence = self.content[1]
        if(self.content[2][0] == '+'):
            self.has_quality_value = True

        if(self.has_quality_value):
            self.quality_value = self.content[2]

class SequenceType(Enum):
    Fasta = 1
    Multi_Fasta = 2
    FastQ = 3

class SequenceParser:

    def parse(self, seq_type, content, seq_name):

        if(seq_type == SequenceType.Fasta):
            return Fasta_Sequence(content, seq_name)
        elif(seq_type == SequenceType.Multi_Fasta):
            return Multi_Fasta_Sequence(content, seq_name)
        elif(seq_type == SequenceType.FastQ):
            return FastaQ_Sequence(content, seq_name)



def main():
    #with open('data/multi_fasta.mfa', 'r') as output_data:
    #    test = Multi_Fasta_Sequence("name1", [output_data])
    #    test.parse()
    f = open('data/multi_fasta.mfa', 'r')
    output_data = f.readlines()
    f.close()
    parser = SequenceParser()
    #test = parser.parse(SequenceType.Multi_Fasta, output_data, "test1")
    test = Multi_Fasta_Sequence(output_data, "test")
    test.parse()
    print(test.name)

    f2 = open('data/SRR081241.filt.fastq', 'r')
    output_data = f2.readlines()
    f2.close()
    test2 = FastaQ_Sequence(output_data)
    test2.parse()
    print(test2.sequence)

    f3 = open('data/fasta.fa', 'r')
    output_data = f3.readlines()
    f3.close()

    test3 = Fasta_Sequence(output_data)
    test3.parse()
    #print(test3.sequence)
    #print(test3.name)



if __name__ == "__main__":
    main()                 