import itertools
from typing import List, Tuple
import numpy as np
import heapq 
from container import Container
from copy import deepcopy
from ship import ship

    
class Cell:
    def __init__(self, position, isFilled, container = None):
        self.isFilled = isFilled
        self.position = position
        self.container = container  # A Container object, or None if empty
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
        Container("S", 20),  # Container A with weight 10
        Container("A", 5),  # Container B with weight 15
        Container("UNUSED", 0),   # Container C with weight 5
        Container("UNUSED", 0),  # Container D with weight 20
        Container("D", 0),  # Container E with weight 12
        Container("K", 0),   # Container F with weight 8
        Container("X", 15),   # Container G with weight 7
        Container("C", 0),  # Container H with weight 18
        Container("ee", 0),  # Container I with weight 12
        Container("Z", 0),   # Container J with weight 8
        Container("w", 0),   # Container K with weight 7
        Container("WEEAE", 0)   # Container L with weight 18
    ]

    ship_matrix = np.zeros((3, 4), dtype=int) 
    my_ship = ship(ship_matrix)



    
    positions = [(0, 0), (0, 1), (0, 2), (0, 3), 
                 (1, 0), (1, 1), (1, 2), (1, 3),
                 (2, 0), (2, 1), (2, 2), (2, 3)]



    for container, position in zip(containers, positions):
        my_ship.addContainers(position, container)

    cells = []
    for pos in positions:
        # Check if a container exists at this position
        container = my_ship.shipDict.get(tuple(pos), None)
        isFilled = container is not None
        # Create a Cell, passing the container if it exists
        cells.append(Cell(position=pos, isFilled=isFilled, container=container))

    
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
        mid = ship.columns // 2  # Middle column for determining left/right weights

        # Function to compute weights on the left and right sides
        def compute_weights(cellList):
            left_weight = sum(
                cell.container.weight
                for cell in cellList if cell.isFilled and cell.position[1] < mid
            )
            right_weight = sum(
                cell.container.weight
                for cell in cellList if cell.isFilled and cell.position[1] >= mid
            )
            return left_weight, right_weight

                # Function to print the grid
        def print_grid(cellList):
            # Initialize the grid with '0' for empty cells
            grid = [['0' for _ in range(ship.columns)] for _ in range(ship.rows)]

            # Populate grid with container weights for filled cells
            for cell in cellList:
                row, col = cell.position
                if cell.isFilled:
                    grid[row][col] = str(cell.container.weight)

            # Print the grid
            print("Grid:")
            for row in grid:
                print(' '.join(cell.ljust(2) for cell in row))  # Ensure consistent alignment
            print()

        # Total weight computation
        def total_weight(cellList):
            return sum(
                cell.container.weight 
                for cell in cellList if cell.isFilled
            )

        # Initial state and setup
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
            if abs(currLeftWeight - currRightWeight) <= 0.1 * currRightWeight:
                print(f"Balanced: Left = {currLeftWeight}, Right = {currRightWeight}")
                optimal_path = path + [currentCellList]
                
                print("\nOptimal Path Grids:")
                for i, grid_state in enumerate(optimal_path):
                    print(f"Step {i}:")
                    print_grid(grid_state)
                
                return True

            # Create a state key to avoid revisiting
            state_key = tuple(
                sorted((tuple(cell.position), cell.isFilled) for cell in currentCellList)
            )
            if state_key in closed_set:
                continue
            closed_set.add(state_key)

            # Try moving each filled container
            for cell in currentCellList:
                if not cell.isFilled:
                    continue

                col = cell.position[1]
                # Check if any container blocks this one from being moved
                if any(currCell.isFilled and currCell.position[1] == col and currCell.position[0] < cell.position[0]
                    for currCell in currentCellList):
                    continue  # Skip if a container blocks the movement

                cellContainerWeight = cell.container.weight

                # Try moving to each other column
                for targetCol in range(ship.columns):
                    if targetCol == col:
                        continue

                    # Find the next empty row in the target column
                    targetRow = findNextEmptyRow(currentCellList, targetCol)
                    if targetRow is None:
                        continue  # Skip if no space

                    # Create a new state by moving the container
                    newCellList = deepcopy(currentCellList)

                    for c in newCellList:
                        if c.position == cell.position:  # Move the container
                            c.position = (targetRow, targetCol)
                        elif c.position == (targetRow, targetCol):  # Vacate the target cell
                            c.isFilled = False
                            c.container.weight = 0   # Clear the container

                    # Compute new weights
                    newLeftWeight, newRightWeight = compute_weights(newCellList)
                    h_cost = abs(newLeftWeight - newRightWeight)

                    # Add to exploration set
                    new_path = path + [newCellList]
                    heapq.heappush(open_set, (h_cost, (newCellList, newLeftWeight, newRightWeight, new_path)))

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