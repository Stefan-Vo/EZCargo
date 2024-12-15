    
class Cell:
    def __init__(self, position):
        self.isFilled = False
        self.position = position
        self.h = float("inf")
        self.g = 0
        self.totalCost = self.g + self.h

    def addPosition(self, position):
        self.positionList.append(position)



positions = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3),(2,0),(2,1),(2,2),(2,3)]

cells = [Cell(pos) for pos in positions]

for c in cells:
    print(c.position)