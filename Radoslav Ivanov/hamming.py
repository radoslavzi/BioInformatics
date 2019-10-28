class Hamming:
    def __init__(self, str1, str2):

        if len(str1) != len(str2):
            raise AssertionError("Both strings should be same size")

        self.str1 = str1
        self.str2 = str2
    
    def calculateDistance(self):
        result = 0
        for i in range(0, len(self.str1)):
            if self.str1[i] != self.str2[i]:
                result += 1

        return result

file = open('data/hamming.txt', 'r')
str1 = file.readline().strip()
str2 = file.readline().strip()
file.close()
hm = Hamming(str1, str2)
distance = hm.calculateDistance()

print(distance)