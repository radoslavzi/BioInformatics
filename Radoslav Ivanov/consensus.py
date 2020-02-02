from numpy as np

class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix
        
    def calculateProfile(self):
        profile = np.array([],[],[],[])
        
        for row in self.matrix:
            for col in row:
                profile[self.matrix.index(row)].append()