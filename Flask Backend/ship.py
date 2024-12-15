from container import Container
class ship:
    def __init__(self,matrix):
        self.matrix = matrix
        self.rows = len(matrix)
        self.columns = len(matrix[1])
        self.shipDict = {}
    def __iter__(self):
        for row in self.matrix:
            yield row
    def addContainers(self,position,Container):
        self.shipDict[tuple(position)] = Container
    def displayContainers(self):
        print("\nCurrent Ship Grid:")
        for i in range(self.matrix.shape[0]):
            row = []
            for j in range(self.matrix.shape[1]):
                pos = (i, j)
                if pos in self.shipDict:
                    container = self.shipDict[pos]
                    row.append(container.id if container else "Empty")
                else:
                    row.append("Empty")
            print(" | ".join(row))
    def __len__(self):
        return len(self.shipDict)


# [01,01], {00000}, NAN
# [01,02], {00099}, Cat
# [01,03], {00100}, Dog
# [01,04], {00000}, UNUSED
# [01,05], {00000}, UNUSED
# [01,06], {00000}, UNUSED
# [01,07], {00000}, UNUSED
# [01,08], {00000}, UNUSED
# [01,09], {00000}, UNUSED
# [01,10], {00000}, UNUSED
# [01,11], {00000}, UNUSED
# [01,12], {00000}, NAN
# [02,01], {00000}, UNUSED
# [02,02], {00000}, UNUSED
# [02,03], {00000}, UNUSED
# [02,04], {00000}, UNUSED
# [02,05], {00000}, UNUSED
# [02,06], {00000}, UNUSED
# [02,07], {00000}, UNUSED
# [02,08], {00000}, UNUSED
# [02,09], {00000}, UNUSED
# [02,10], {00000}, UNUSED
# [02,11], {00000}, UNUSED
# [02,12], {00000}, UNUSED


