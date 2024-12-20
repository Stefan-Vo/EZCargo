import itertools
from typing import List, Tuple
import numpy as np
import heapq 
from container import Container
from copy import deepcopy
from ship import ship
import math
    
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
    

class Buffer:
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
        return f"Buffer {self.isFilled, self.position}"
    
    def __lt__(self,other):
            return self.position < other.position


def main():
    containers = [
        Container("S", 20),  # Container A with weight 10
        Container("A", 5),  # Container B with weight 15
        Container("UNUSED", 0),   # Container C with weight 5
        Container("CASEY", 0),  # Container D with weight 20
        Container("D", 0),  # Container E with weight 12
        Container("K", 0),   # Container F with weight 8
        Container("X", 15),   # Container G with weight 7
        Container("C", 0),  # Container H with weight 18
        Container("ee", 0),  # Container I with weight 12
        Container("Z", 0),   # Container J with weight 8
        Container("w", 0),   # Container K with weight 7
        Container("WEEAE", 0)   # Container L with weight 18
    ]

    ship_matrix = np.zeros((8, 12), dtype=int) 
    my_ship = ship(ship_matrix)


    
    
    positions = [(i, j) for i in range(1, 9) for j in range(1, 13)]

    

    buffer = []
    for pos in positions:
        container = my_ship.shipDict.get(tuple(pos), None)
        print(f"Position {pos}: Container = {container}")
        isFilled = container is not None
        bufferGrid = Buffer(pos, isFilled=isFilled, container=Container("UNUSED", 0)) #change later
        buffer.append(bufferGrid)


    for container, position in zip(containers, positions):
        my_ship.addContainers(position, container)

    cells = []
    for pos in positions:
        # Check if a container exists at this position and has a meaningful weight
        container = my_ship.shipDict.get(tuple(pos))
        if container.id != "UNUSED":
            container.isFilled = True
        # Create a Cell, passing the container if it exists and has weight
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
    
    def balanceContainers(ship, cellList, buffer):
        mid = ship.columns // 2  # Middle column for determining left/right weights
        print(type(ship), type(cellList), type(buffer))
        # Compute the left and right weight sums
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

        # Print grid representation
        def print_grid(cellList):
            # Initialize a grid with placeholder values
            grid = [['a' for _ in range(ship.columns)] for _ in range(ship.rows)]
            
            for i, cell in enumerate(cellList):
                row, col = cell.position
                if cell.isFilled:
                    # Format: "weight(isFilled)"
                    grid[row][col] = f"{cell.container.weight}({cell.isFilled})"
                else:
                    # If not filled, just put "empty(isFilled)"
                    grid[row][col] = f"empty({cell.isFilled})"

            # Print the grid
            print("Grid:")
            for row in grid:
                print(' '.join(str(cell).ljust(15) for cell in row))  # Adjust the width for proper alignment
            print()

        # Print buffer grid representation
        def print_buffer(bufferList):
            grid = [['0' for _ in range(4)] for _ in range(3)]  # 3x4 buffer grid
            for buff in bufferList:
                row, col = buff.position
                if buff.isFilled:
                    grid[row][col] = str(buff.container.weight)

            print("Buffer:")
            for row in grid:
                print(' '.join(str(cell).ljust(2) for cell in row))  # Ensure proper alignment
            print()

        # Total weight computation
        def total_weight(cellList):
            return sum(
                cell.container.weight
                for cell in cellList if cell.isFilled
            )

        # Check if the main grid is full
        def is_main_grid_full(cellList):
            return all(cell.isFilled for cell in cellList)

        # Move container from buffer to main grid
        def move_from_buffer(currentCellList, buffer):
            for buff in buffer:
                if buff.isFilled and buff.container is not None:
                    empty_cell = next(
                        (cell for cell in currentCellList if not cell.isFilled),
                        None
                    )
                    if empty_cell:
                        # print(f"Moving container from buffer {buff.position}")
                        # print(f"Buffer container BEFORE move: {buff.container}")
                        # print(f"Empty cell BEFORE move: {empty_cell.container}")
                        
                        # Explicitly copy container attributes instead of using deepcopy
                        temp = deepcopy(empty_cell.container.weight)
                        empty_cell.container = deepcopy(buff.container)
                        empty_cell.isFilled = True
                        
                        # print(f"Buffer container DURING move: {buff.container}")
                        # print(f"Empty cell AFTER move: {empty_cell.container}")
                        # print(f"Empty cell position AFTER move: {empty_cell.position}")
                        print("MOVE FROM BUFFER",  empty_cell.container.weight)
                        print_buffer(buffer)
                        
                        # Clear the buffer slot
                        buff.isFilled = False
                        buff.container.weight = temp
                        print(f"Buffer slot AFTER move: {buff}")
                        
                        return True
            return False


        # Move container from main grid to buffer
        def move_to_buffer(currentCellList, buffer):
            for cell in currentCellList:
                if cell.isFilled:
                    empty_buffer_slot = next(
                        (buff for buff in buffer if not buff.isFilled),
                        None
                    )
                    if empty_buffer_slot:
                        print("MOVE", cell.container.weight, cell.position)
                        print("Cell in buffer", cell.container.weight)
                        temp = deepcopy(empty_buffer_slot.container.weight)
                        empty_buffer_slot.container = deepcopy(cell.container) #20
                        empty_buffer_slot.isFilled = True
                        cell.isFilled = False
                        cell.container.weight = temp #Empty
                        print("AFTER BUFFER",  cell.container.weight)
                        print_buffer(buffer)
                        return True
            return False

        # Initialize the state
        initial_total_weight = total_weight(cellList)
        left_weight, right_weight = compute_weights(cellList)

        open_set = []
        initial_state = (deepcopy(cellList), left_weight, right_weight, [], deepcopy(buffer))
        heapq.heappush(open_set, (0, initial_state))
        closed_set = set()

        while open_set:
            h_, (currentCellList, currLeftWeight, currRightWeight, path, bufferList) = heapq.heappop(open_set)
            currLeftWeight = int(currLeftWeight)
            currRightWeight = int(currRightWeight)
            print("WWWWWWWWWWWWW", currLeftWeight, currRightWeight)
            # Check if balanced
            if abs(currLeftWeight - currRightWeight) <= 0.1 * currRightWeight:
                print(f"Balanced: Left = {currLeftWeight}, Right = {currRightWeight}")
                optimal_path = path + [currentCellList]
                print("\nOptimal Path Grids:")
                for i, grid_state in enumerate(optimal_path):
                    print(f"Step {i}:")
                    print_grid(grid_state)
                return True

            # Try moving containers from buffer if the main grid is not full
            if not is_main_grid_full(currentCellList):
                if move_from_buffer(currentCellList, bufferList):
                    currLeftWeight, currRightWeight = compute_weights(currentCellList)
                    print("ZZZZZZZZZZZZZZZZZZZZZZZZZ")
                    print_grid(currentCellList)  # Print grid after moving from buffer

            # If main grid is full, attempt to move containers to buffer
            elif is_main_grid_full(currentCellList):
                if move_to_buffer(currentCellList, bufferList):
                    currLeftWeight, currRightWeight = compute_weights(currentCellList)
                    print("WWWWWWWWWWWWWWWWWW")
                    print_grid(currentCellList)  # Print grid after moving to buffer
                    #print_buffer(bufferList)  # Print buffer state after moving container
                else:
                    continue  # No more room in the buffer
            print_buffer(bufferList)
            # Create a unique state key to avoid revisiting
            state_key = tuple(sorted((tuple(cell.position), cell.isFilled) for cell in currentCellList))
            if state_key in closed_set:
                continue
            closed_set.add(state_key)

            # Try moving containers within the grid
            for cell in currentCellList:
                if not cell.isFilled:
                    continue
                col = cell.position[1] #0,0
                if any(currCell.isFilled and currCell.position[1] == col and currCell.position[0] < cell.position[0]
                        for currCell in currentCellList):
                    continue
                # Try moving the container to another column
                for targetCol in range(ship.columns):
                    if targetCol == col:
                        continue

                    targetRow = findNextEmptyRow(currentCellList, targetCol)
                    if targetRow is None:
                        continue  # No empty row available in this column

                    
                    newCellList = deepcopy(currentCellList)

                    # Find the target cell
                    for c in newCellList:
                        if c.position == (targetRow, targetCol):
                            target_cell = c
                            break
                    print("TARGET CELL: ", target_cell)
                    # Move the container to the target cell
                    if cell.position == target_cell.position:
                        print("WEWAD", cell, target_cell)
                        continue
                 

                    #target_cell is empty cell??
                    for c in newCellList:
                        if c.position == cell.position:
                            print("FIRST", c.position, c.container.weight)
                            temp = deepcopy(c) #0,1
                            c.position = deepcopy(target_cell.position) # c becomes 0,0 with weight of target_cell 0
                            #c.container.weight = temp.container.weight
                            #target_cell.container.weight = deepcopy(temp.container.weight) #
                            target_cell.position = deepcopy(temp.position)
                            print("TARGET_CELL", target_cell.position, target_cell.container.weight)
                            target_cell.isFilled = False
                            c.isFilled = True
                            print("AFTRER C", c.position, c.container.weight)
                            print("AFTER TARGET_CELL", target_cell.position, target_cell.container.weight)
                            break


                    print_grid(newCellList)

                    #newCellList = deepcopy(currentCellList)
                    newLeftWeight, newRightWeight = compute_weights(newCellList)
                    #print("WWWWWWWWWWWWWW", newLeftWeight, newRightWeight)
                    h_cost = abs(newLeftWeight - newRightWeight)
                    new_path = path + [deepcopy(newCellList)]
                    heapq.heappush(open_set, (h_cost, (newCellList, newLeftWeight, newRightWeight, new_path, bufferList)))

        print("No solution found.")
        return False

    def findNextEmptyRow(cellList, target_col):
        # Check filled cells in the target column from bottom to top
        occupied_rows = set(
            c.position[0] for c in cellList 
            if c.isFilled and c.position[1] == target_col
        )
        
        # Start from the bottom and find the first empty row
        for row in range(2, -1, -1):  
            if row not in occupied_rows:
                return row
        
        # No empty row found
        return None
        
    isBalanced = False #get value from isbalance
    siftCellGrid, siftBufferGrid = cells, buffer
    def sift(isBalanced, siftCellGrid, siftBufferGrid):
        if isBalanced:
            return 
        
        def print_grid(cellList):
            grid = [['0' for _ in range(4)] for _ in range(3)]
            for i, cell in enumerate(cellList):
                row, col = cell.position
                print("BUFFFER") 
                print_buffer(buffer)
                if cell.isFilled:
                    grid[row][col] = str(cell.container.weight)
            print("Grid:")
            for row in grid:
                print(' '.join(str(cell).ljust(2) for cell in row))  # Ensure proper alignment
            print()

        # Print buffer grid representation
        def print_buffer(siftBufferGrid):
            grid = [['0' for _ in range(4)] for _ in range(3)]  # 3x4 buffer grid
            for buff in siftBufferGrid:
                row, col = buff.position
                if buff.isFilled:
                    grid[row][col] = str(buff.container.weight)

            print("Buffer:")
            for row in grid:
                print(' '.join(str(cell).ljust(2) for cell in row))  # Ensure proper alignment
            print()
        def is_main_grid_full(cellList):
            return all(cell.isFilled for cell in cellList)
        
        def move_to_buffer(siftCellGrid, siftBufferGrid):
            # Get all filled cells, sorted by container weight (heaviest first)
            filled_cells = sorted(
                [cell for cell in siftCellGrid if cell.isFilled],
                key=lambda c: c.container.weight,
                reverse=True  # Sort in descending order
            )

            if not filled_cells:
                return False, siftCellGrid, siftBufferGrid  # No containers to move

            for cell in filled_cells:
                # Find an empty buffer slot for the container
                empty_buffer_slot = next((buff for buff in siftBufferGrid if not buff.isFilled), None)
                
                if empty_buffer_slot:
                    # Move the container to the buffer
                    empty_buffer_slot.container = cell.container
                    empty_buffer_slot.isFilled = True
                    cell.isFilled = False
                    cell.container = None  # Clear the cell
                    print(f"Moved container from {cell.position} to buffer at {empty_buffer_slot.position}")
                else:
                    # No more empty buffer slots available
                    break

            return True, siftCellGrid, siftBufferGrid  # Return updated grids

        
        
        
        # def move_from_buffer(siftCellGrid, siftBufferGrid):
        #     filled_buffers = [buff for buff in siftBufferGrid if buff.isFilled]
            
        #     if not filled_buffers:
        #         return False  # No containers to move

        #     for buff in filled_buffers:
        #         empty_cell = next((cell for cell in siftCellGrid if not cell.isFilled), None)
                
        #         if empty_cell:
        #             empty_cell.container = buff.container
        #             empty_cell.isFilled = True
        #             buff.isFilled = False
        #             buff.container = None  # Clear the buffer slot
        #             print(f"Moved container {buff.container} from buffer at {buff.position} to grid at {empty_cell.position}")

            return True      
        
        def move_from_buffer(siftCellGrid, siftBufferGrid):
    
            filled_buffers = [buff for buff in siftBufferGrid if buff.isFilled]

            if not filled_buffers:
                return False  # No containers to move

            # Step 2: Sort containers by weight (heaviest to lightest)
            sorted_buffers = sorted(
                filled_buffers, 
                key=lambda b: b.container.weight, 
                reverse=True
            )

            # Step 3: Define the filling order for the grid (center-first strategy)
            fill_order = []
            row,col= 3,4
            mid=math.floor((col-1)/2)
            for i in range(row):
                fill_order.append((i,mid))
                for j in range(1, mid+1):
                    fill_order.append((i,mid+j))
                    fill_order.append((i,mid-j))
                fill_order.append((i,mid+j+1))


            for i, pos in enumerate(fill_order):
                if i < len(sorted_buffers):  
                    buffer_slot = sorted_buffers[i]
                    target_cell = next(
                        (cell for cell in siftCellGrid if cell.position == pos and not cell.isFilled), 
                        None
                    )
                    if target_cell:
                        target_cell.container = buffer_slot.container
                        target_cell.isFilled = True
                        buffer_slot.isFilled = False
                        buffer_slot.container = None  
                        print(f"Moved container {target_cell.container} to grid at {target_cell.position}")

            return True
        
     

        if move_to_buffer(siftCellGrid, siftBufferGrid):
            print_grid(siftCellGrid)  # Print grid after moving to buffer
            print_buffer(buffer)  # Print buffer state after moving containers
        else:
            return  # No more room in the buffer

        print("AFTER")

           
        if move_from_buffer(siftCellGrid, siftBufferGrid):
            print_grid(siftCellGrid)  # Print grid after moving from buffer
            print_buffer(buffer)  # Print buffer state after moving containers



        print_buffer(buffer)
        return True
        

    # print(sift(isBalanced, siftCellGrid, siftBufferGrid))
    print( totalForEachGrid(my_ship, cells))

    if balanceContainers(my_ship, cells, buffer):
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