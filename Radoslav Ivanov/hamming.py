class Hamming:
    def __init__(self, str1, str2):
        self.str1 = str1
        self.str2 = str2
    
    def calculateDistance(self):
        result = 0
        for i in range(0, len(self.str1)):
            if self.str1[i] != self.str2[i]:
                result += 1

        return result

hm = Hamming('GAGCCTACTAACGGGAT', 'CATCGTAATGACGGCCT')
distance = hm.calculateDistance()

print(distance)