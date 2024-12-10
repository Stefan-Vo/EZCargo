import itertools
from typing import List, Tuple
import numpy as np
import heapq 
from container import Container
from copy import deepcopy
from ship import ship

    
class Cell:
    def __init__(self, position, isFilled):
        self.isFilled = isFilled
        self.position = position
        self.h = float("inf")
        self.g = 0
        self.totalCost = self.g + self.h

    def addPosition(self, position):
        self.positionList.append(position)

    def __str__(self):
        return f"Cell {self.isFilled, self.position}"
    
    def __lt__(self,other):
            return self.position < other.position
    



def main():
    containers = [
        Container("S", 1),  # Container A with weight 10
        Container("A", 15),  # Container B with weight 15
        Container("I", 5),   # Container C with weight 5
        Container("B", 20),  # Container D with weight 20
        Container("D", 12),  # Container E with weight 12
        Container("K", 8),   # Container F with weight 8
        Container("I", 0),   # Container G with weight 7
        Container("C", 0),  # Container H with weight 18
        Container("ee", 0),  # Container I with weight 12
        Container("Z", 0),   # Container J with weight 8
        Container("w", 0),   # Container K with weight 7
        Container("UNUSED", 0)   # Container L with weight 18
    ]

    ship_matrix = np.zeros((3, 4), dtype=int) 
    my_ship = ship(ship_matrix)



    
    positions = [(0, 0), (0, 1), (0, 2), (0, 3), 
                 (1, 0), (1, 1), (1, 2), (1, 3),
                 (2, 0), (2, 1), (2, 2), (2, 3)]

    cells = [Cell(pos, False) for pos in positions]

    for container, position in zip(containers, positions):
        my_ship.addContainers(position, container)


    
    def printOriginalMatrix():
        matrix = np.zeros((3, my_ship.columns), dtype=int)

        for position, container in my_ship.shipDict.items():
            row, col = position
            matrix[row, col] = container.weight

        print(" (with positions):")
        print(matrix)

    def totalForEachGrid(ship, cellList):
        newEmptyCellList = []

        for cell in cellList:
            if tuple(cell.position) in ship.shipDict and ship.shipDict[tuple(cell.position)].id != "UNUSED":
                cell.isFilled = True
            else:
                cell.isFilled = False

        rows = 3
        cols = 4


        for cell in cellList:
            row, col = cell.position # (0,0) first pass
            cell.h = 0

            for r in range(row-1, -1 , -1):
                above_cell = next((c for c in cellList if c.position == (r,col)), None)
                if above_cell and above_cell.isFilled:
                    cell.h += 1
            print(cell.position, cell.h, cell.isFilled)

    #print(totalForEachGrid(my_ship, cells))
        


    
    #totalForEachGrid(my_ship, cells)
    
    def balanceContainers(ship, cellList):
        mid = ship.columns // 2
        
        def compute_weights(cellList):
            left_weight = sum(
                ship.shipDict[tuple(cell.position)].weight
                for cell in cellList if cell.isFilled and cell.position[1] < mid
            )
            right_weight = sum(
                ship.shipDict[tuple(cell.position)].weight
                for cell in cellList if cell.isFilled and cell.position[1] >= mid
            )
            return left_weight, right_weight

        def print_grid(cellList):
            # grid with all original positions
            grid = [[' ' for _ in range(ship.columns)] for _ in range(ship.rows)]
            
            #  grid with weights for filled cells
            for cell in cellList:
                # if cell.isFilled:
                row, col = cell.position
                grid[row][col] = str(ship.shipDict[tuple(cell.position)].weight)
            
            print("Grid:")
            for row in grid:
                print(' '.join(str(cell).ljust(2) for cell in row))
            print()

        def total_weight(cellList):
            return sum(
                ship.shipDict[tuple(cell.position)].weight 
                for cell in cellList if cell.isFilled
            )

        # Initial weight check
        initial_total_weight = total_weight(cellList)
        left_weight, right_weight = compute_weights(cellList)

        open_set = []
        initial_state = (deepcopy(cellList), left_weight, right_weight, [])
        heapq.heappush(open_set, (0, initial_state))
        closed_set = set()

        while open_set:
            h_, (currentCellList, currLeftWeight, currRightWeight, path) = heapq.heappop(open_set)
            currLeftWeight = int(currLeftWeight)
            currRightWeight = int(currRightWeight)

            # Check if balanced
            if abs(currLeftWeight - currRightWeight) <= 0.1 * initial_total_weight:
                print(f"Balanced: Left = {currLeftWeight}, Right = {currRightWeight}")
                optimal_path = path + [currentCellList]
                
                print("\nOptimal Path Grids:")
                for i, grid_state in enumerate(optimal_path):
                    print(f"Step {i}:")
                    print_grid(grid_state)
                
                return True

            # Create a state key to avoid revisiting
            initialStateKey = tuple(
                (tuple(cell.position), cell.isFilled) for cell in currentCellList
            )
            if initialStateKey in closed_set:
                continue
            closed_set.add(initialStateKey)

            # Try moving each filled container
            for cell in currentCellList:
                if not cell.isFilled:
                    continue

                col = cell.position[1]
                # CHECK IF ANY CONTAINSERS BELOW THIS CURR CONTAINER IN SAME COL IF THERE IS WE CANT MOVE YET SICNE HTE ONBE ABOVE HAS BE MOVE FIRST!
                if any(
                    currCell.isFilled and currCell.position[1] == col and currCell.position[0] < cell.position[0]
                    for currCell in currentCellList
                ):
                    continue
                # IF NOT FOUND LOOP SKIPS TO NEXT ITERATION SINCE CURR CELL CANT BE MOVE UNFORTUNATE

                cellContainerWeight = ship.shipDict[tuple(cell.position)].weight

                # Try moving to each other column
                for targetCol in range(ship.columns):
                    if targetCol == col:
                        continue

                    # Find the next empty row in the target column
                    targetRow = findNextEmptyRow(currentCellList, targetCol)
                    if targetRow is None:
                        continue  # Skip if no space

                    # Create a new list with the container moved
                    newCellList = []


                    target_cell = next((cell for cell in currentCellList if cell.position == (targetRow, col)), None) #FIND THE TARFVETGE CELL 

                    cell_moved = False
                    for c in currentCellList:
                        if c.position == cell.position and not cell_moved:
                            # Create a new cell with updated position
                            new_cell = deepcopy(c)
                            new_cell.position = (targetRow, targetCol)
                            new_cell.isFilled = True  # Ensure it's marked as filled
                            newCellList.append(new_cell)

                            temp = ship.shipDict[(tuple((targetRow, targetCol)))].weight # NEED TO SWAP RIGHT SO WE NEED HOLD THIS
                            # Move the container: update its position in the ship's container dictionary
                            # Find the container associated with the original cell position
                            temp2 = ship.shipDict[(tuple(c.position))].weight
                            ship.shipDict[(tuple((targetRow, targetCol)))].weight = temp2
                            ship.shipDict[(tuple(c.position))].weight = temp
                            
                            # Mark the original cell as empty
                            empty_cell = deepcopy(target_cell)
                            empty_cell.isFilled = False  # Mark the original position as empty
                            empty_cell.position = c.position  # Keep original position
                            newCellList.append(empty_cell)

                            cell_moved = True
                        else:
                            # Add all other cells as they were
                            newCellList.append(deepcopy(c))


                    # Compute new weights
                    #if col < mid:
                        #newLeftWeight = currLeftWeight - cellContainerWeight
                        #newRightWeight = currRightWeight + cellContainerWeight
                    #else:
                        #newLeftWeight = currLeftWeight + cellContainerWeight
                        #newRightWeight = currRightWeight - cellContainerWeight

                    # Compute heuristic cost (difference between left and right weights)
                    newLeftWeight, newRightWeight = compute_weights(newCellList)
                    h_cost = abs(newLeftWeight - newRightWeight)
                    
                    # Add to exploration set
                    new_path = path + [currentCellList]
                    heapq.heappush(open_set, (h_cost ,(newCellList, newLeftWeight, newRightWeight, new_path)))

        print("No solution found.")
        return False
        

    def findNextEmptyRow(cellList, target_col):
        # Check filled cells in the target column from bottom to top
        occupied_rows = set(
            c.position[0] for c in cellList 
            if c.isFilled and c.position[1] == target_col
        )
        
        #Start from the bot 
        for row in range(2, -1, -1):  
            if row not in occupied_rows:
                return row
        
        # nein row
        return None
        

    print( totalForEachGrid(my_ship, cells))

    if balanceContainers(my_ship, cells):
        print("Balanced")
    else:
        print("Not Blaanced")
    
    



    def printBalanceMatrix():
        matrix = np.zeros((3, my_ship.columns), dtype=int)
        
        for position, container in my_ship.shipDict.items():
            row, col = position
            matrix[row, col] = container.weight
        
        print("Balance Matrix:")
        print(matrix)
        
        left_total = np.sum(matrix[:, [0,1]])
        right_total = np.sum(matrix[:, [2,3]])

     

        total_weight = left_total + right_total
        
        percentage_difference = abs(left_total - right_total) / total_weight * 100
        
        print(f"\nLeft Total: {left_total}")
        print(f"Right Total: {right_total}")
        print(f"Percentage Difference: {percentage_difference:.2f}%")

    #printOriginalMatrix()
    
    #balanceContainers(my_ship, cells)
    
    #printBalanceMatrix()

    my_ship.displayContainers()

if __name__ == "__main__":
    main()