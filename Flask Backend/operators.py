import itertools
from typing import List, Tuple
import numpy as np
import heapq 
from container import Container
from copy import deepcopy
from ship import ship
import math
import pandas as pd

    
class Cell:
    def __init__(self, position, isFilled, container = None):
        self.isFilled = isFilled
        self.position = position
        self.container = container  # Container object OR None if empty
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
        self.container = container  
        self.h = float("inf")
        self.g = 0
        self.totalCost = self.g + self.h

    def addPosition(self, position):
        self.positionList.append(position)

    def __str__(self):
        return f"Buffer {self.isFilled, self.position}"
    
    def __lt__(self,other):
            return self.position < other.position

def balanceContainers(ship, cellList, buffer):
    mid = ship.columns // 2  # Middle column for determining left/right weights
    print(type(ship), type(cellList), type(buffer))
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

    def print_grid(cellList):
        grid = [['a' for _ in range(13)] for _ in range(9)]
        
        for i, cell in enumerate(cellList):
            row, col = cell.position
            if cell.isFilled:
                # Format: "weight(isFilled)"
                grid[row][col] = f"{cell.container.weight}({cell.isFilled})"
            else:
                grid[row][col] = f"UNUSED({cell.isFilled})"

        # Print the grid
        print("Grid:")
        for row in grid:
            print(' '.join(str(cell).ljust(15) for cell in row))  # adjust the width for proper alignment
        print()

    # Print buffer grid representation
    def print_buffer(bufferList):
        grid = [['0' for _ in range(13)] for _ in range(9)]  
        for buff in bufferList:
            row, col = buff.position
            if buff.isFilled:
                grid[row][col] = str(buff.container.weight)

        print("Buffer:")
        for row in grid:
            print(' '.join(str(cell).ljust(2) for cell in row))  
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


    # mooove container from main grid to buffer
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
    def generate_neighbors(currentCellList, left_weight, right_weight, path, bufferList):
        neighbors = []
        for cell in currentCellList:
            if not cell.isFilled or cell.container.id == "UNUSED":
                continue
                
            col = cell.position[1]
            
            for targetCol in range(ship.columns):
                if targetCol == col:
                    continue
                    
                targetRow = findNextEmptyRow(currentCellList, targetCol)
                if targetRow is None:
                    continue
                    
                # newstate from new move
                newCellList = deepcopy(currentCellList)
                
                # find source and target cells in new state
                source_cell = next(c for c in newCellList if c.position == cell.position)
                target_cell = next(c for c in newCellList if c.position == (targetRow, targetCol))
                
                # move container
                target_cell.container = source_cell.container
                target_cell.isFilled = True
                source_cell.container = Container("UNUSED", 0)
                source_cell.isFilled = False
                
                # calculate the nbew weights
                new_left_weight, new_right_weight = compute_weights(newCellList)
                
                neighbors.append((new_left_weight, new_right_weight, newCellList, path + [newCellList], bufferList))
                
        return neighbors
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
                apply_gravity(cellList)
            return True  # exit because balsanced found

        # create a unique state key to avoid revisiting so no loops
        state_key = tuple(sorted((tuple(cell.position), cell.isFilled) for cell in currentCellList))
        if state_key in closed_set:
            continue
        closed_set.add(state_key)
        
        # print_grid(currentCellList)  # Optionally, visualize the current grid state

        # Generate neighbors by trying valid moves
        neighbors = generate_neighbors(currentCellList, currLeftWeight, currRightWeight, path, bufferList)
        
        for neighbor in neighbors:
            newLeftWeight, newRightWeight, newCellList, newPath, newBuffer = neighbor
            
            # Calculate the heuristic cost (h) for the neighbor using weight here
            h_cost = abs(newLeftWeight - newRightWeight)  
            
            # add the neighbor state to the open set
            heapq.heappush(open_set, (h_cost, (newCellList, newLeftWeight, newRightWeight, newPath, newBuffer)))

    print("No solution found.")
    return False

def findNextEmptyRow(cellList, target_col):
    # get all cells in this col
    column_cells = [cell for cell in cellList if cell.position[1] == target_col]
    
    # move to lowest positiion if possible
    for cell in column_cells:
        if cell.isFilled and cell.container.id != "UNUSED":
            # finding lowest empty position below this container
            lowest_empty = None
            for row in range(1, cell.position[0]):  
                current_cell = next((c for c in column_cells if c.position[0] == row), None)
                if current_cell and not current_cell.isFilled:
                    lowest_empty = current_cell
            
            # If found lowest should move the container there
            if lowest_empty:
                lowest_empty.container = cell.container
                lowest_empty.isFilled = True
                cell.container = Container("UNUSED", 0)
                cell.isFilled = False
    
    # now find the lowest empty position for new container
    for row in range(1, my_ship.rows + 1):
        current_cell = next((c for c in column_cells if c.position[0] == row), None)
        if current_cell and not current_cell.isFilled:
            return row

    return None
    
    
def main():
    containers = [
        Container("NAN", 0),  # [01,01], {00000}, NAN
        Container("Catfish", 60),  # [01,02], {00060}, Catfish
        Container("Dogana", 20),  # [01,03], {00020}, Dogana
        Container("Batons", 20),  # [01,04], {00020}, Batons
        Container("UNUSED", 0),  # [01,05], {00000}, UNUSED
        Container("UNUSED", 0),  # [01,06], {00000}, UNUSED
        Container("UNUSED", 0),  # [01,07], {00000}, UNUSED
        Container("UNUSED", 0),  # [01,08], {00000}, UNUSED
        Container("UNUSED", 0),  # [01,09], {00000}, UNUSED
        Container("UNUSED", 0),  # [01,10], {00000}, UNUSED
        Container("UNUSED", 0),  # [01,11], {00000}, UNUSED
        Container("NAN", 0),  # [01,12], {00000}, NAN
        Container("UNUSED", 0),  # [02,01], {00000}, UNUSED
        Container("Rations for US Army", 20),  # [02,02], {00020}, Rations for US Army
        Container("UNUSED", 0),  # [02,03], {00000}, UNUSED
        Container("UNUSED", 0),  # [02,04], {00000}, UNUSED
        Container("UNUSED", 0),  # [02,05], {00000}, UNUSED
        Container("UNUSED", 0),  # [02,06], {00000}, UNUSED
        Container("UNUSED", 0),  # [02,07], {00000}, UNUSED
        Container("UNUSED", 0),  # [02,08], {00000}, UNUSED
        Container("UNUSED", 0),  # [02,09], {00000}, UNUSED
        Container("UNUSED", 0),  # [02,10], {00000}, UNUSED
        Container("UNUSED", 0),  # [02,11], {00000}, UNUSED
        Container("UNUSED", 0),  # [02,12], {00000}, UNUSED
        Container("UNUSED", 0),  # [03,01], {00000}, UNUSED
        Container("UNUSED", 0),  # [03,02], {00000}, UNUSED
        Container("UNUSED", 0),  # [03,03], {00000}, UNUSED
        Container("UNUSED", 0),  # [03,04], {00000}, UNUSED
        Container("UNUSED", 0),  # [03,05], {00000}, UNUSED
        Container("UNUSED", 0),  # [03,06], {00000}, UNUSED
        Container("UNUSED", 0),  # [03,07], {00000}, UNUSED
        Container("UNUSED", 0),  # [03,08], {00000}, UNUSED
        Container("UNUSED", 0),  # [03,09], {00000}, UNUSED
        Container("UNUSED", 0),  # [03,10], {00000}, UNUSED
        Container("UNUSED", 0),  # [03,11], {00000}, UNUSED
        Container("UNUSED", 0),  # [03,12], {00000}, UNUSED
        Container("UNUSED", 0),  # [04,01], {00000}, UNUSED
        Container("UNUSED", 0),  # [04,02], {00000}, UNUSED
        Container("UNUSED", 0),  # [04,03], {00000}, UNUSED
        Container("UNUSED", 0),  # [04,04], {00000}, UNUSED
        Container("UNUSED", 0),  # [04,05], {00000}, UNUSED
        Container("UNUSED", 0),  # [04,06], {00000}, UNUSED
        Container("UNUSED", 0),  # [04,07], {00000}, UNUSED
        Container("UNUSED", 0),  # [04,08], {00000}, UNUSED
        Container("UNUSED", 0),  # [04,09], {00000}, UNUSED
        Container("UNUSED", 0),  # [04,10], {00000}, UNUSED
        Container("UNUSED", 0),  # [04,11], {00000}, UNUSED
        Container("UNUSED", 0),  # [04,12], {00000}, UNUSED
        Container("UNUSED", 0),  # [05,01], {00000}, UNUSED
        Container("UNUSED", 0),  # [05,02], {00000}, UNUSED
        Container("UNUSED", 0),  # [05,03], {00000}, UNUSED
        Container("UNUSED", 0),  # [05,04], {00000}, UNUSED
        Container("UNUSED", 0),  # [05,05], {00000}, UNUSED
        Container("UNUSED", 0),  # [05,06], {00000}, UNUSED
        Container("UNUSED", 0),  # [05,07], {00000}, UNUSED
        Container("UNUSED", 0),  # [05,08], {00000}, UNUSED
        Container("UNUSED", 0),  # [05,09], {00000}, UNUSED
        Container("UNUSED", 0),  # [05,10], {00000}, UNUSED
        Container("UNUSED", 0),  # [05,11], {00000}, UNUSED
        Container("UNUSED", 0),  # [05,12], {00000}, UNUSED
        Container("UNUSED", 0),  # [06,01], {00000}, UNUSED
        Container("UNUSED", 0),  # [06,02], {00000}, UNUSED
        Container("UNUSED", 0),  # [06,03], {00000}, UNUSED
        Container("UNUSED", 0),  # [06,04], {00000}, UNUSED
        Container("UNUSED", 0),  # [06,05], {00000}, UNUSED
        Container("UNUSED", 0),  # [06,06], {00000}, UNUSED
        Container("UNUSED", 0),  # [06,07], {00000}, UNUSED
        Container("UNUSED", 0),  # [06,08], {00000}, UNUSED
        Container("UNUSED", 0),  # [06,09], {00000}, UNUSED
        Container("UNUSED", 0),  # [06,10], {00000}, UNUSED
        Container("UNUSED", 0),  # [06,11], {00000}, UNUSED
        Container("UNUSED", 0),  # [06,12], {00000}, UNUSED
        Container("UNUSED", 0),  # [07,01], {00000}, UNUSED
        Container("UNUSED", 0),  # [07,02], {00000}, UNUSED
        Container("UNUSED", 0),  # [07,03], {00000}, UNUSED
        Container("UNUSED", 0),  # [07,04], {00000}, UNUSED
        Container("UNUSED", 0),  # [07,05], {00000}, UNUSED
        Container("UNUSED", 0),  # [07,06], {00000}, UNUSED
        Container("UNUSED", 0),  # [07,07], {00000}, UNUSED
        Container("UNUSED", 0),  # [07,08], {00000}, UNUSED
        Container("UNUSED", 0),  # [07,09], {00000}, UNUSED
        Container("UNUSED", 0),  # [07,10], {00000}, UNUSED
        Container("UNUSED", 0),  # [07,11], {00000}, UNUSED
        Container("UNUSED", 0),  # [07,12], {00000}, UNUSED
        Container("UNUSED", 0),  # [08,01], {00000}, UNUSED
        Container("UNUSED", 0),  # [08,02], {00000}, UNUSED
        Container("UNUSED", 0),  # [08,03], {00000}, UNUSED
        Container("UNUSED", 0),  # [08,04], {00000}, UNUSED
        Container("UNUSED", 0),  # [08,05], {00000}, UNUSED
        Container("UNUSED", 0),  # [08,06], {00000}, UNUSED
        Container("UNUSED", 0),  # [08,07], {00000}, UNUSED
        Container("UNUSED", 0),  # [08,08], {00000}, UNUSED
        Container("UNUSED", 0),  # [08,09], {00000}, UNUSED
        Container("UNUSED", 0),  # [08,10], {00000}, UNUSED
        Container("UNUSED", 0),  # [08,11], {00000}, UNUSED
        Container("UNUSED", 0),  # [08,12], {00000}, UNUSED
    ]

    # Updated positions to be in the same pattern as the containers
    positions = [(i, j) for i in range(1, 9) for j in range(1, 13)]

    ship_matrix = np.zeros((8, 12), dtype=int)  # Updated ship matrix for 8 rows and 12 columns
    my_ship = ship(ship_matrix)

    buffer = []
    for pos in positions:
        container = my_ship.shipDict.get(tuple(pos), None)
        print(f"Position {pos}: Container = {container}")
        isFilled = container is not None
        bufferGrid = Buffer(pos, isFilled=isFilled, container=Container("UNUSED", 0))  # Change later
        buffer.append(bufferGrid)

    for container, position in zip(containers, positions):
        my_ship.addContainers(position, container)

    cells = []
    for pos in positions:
        container = my_ship.shipDict.get(tuple(pos))
        isFilled = container is not None and container.id != "UNUSED"
        # create a Cell give passing the container if it exists and has a weight
        cells.append(Cell(position=pos, isFilled=isFilled, container=container if container else Container("UNUSED", 0)))

    
    def printOriginalMatrix():
        matrix = np.zeros((8, my_ship.columns), dtype=int)

        for position, container in my_ship.shipDict.items():
            row, col = position
            matrix[row, col] = container.weight

        print(" (with positions):")
        print(matrix)

    # def totalForEachGrid(ship, cellList):
    #     newEmptyCellList = []

    #     for cell in cellList:
    #         if tuple(cell.position) in ship.shipDict and ship.shipDict[tuple(cell.position)].id != "UNUSED":
    #             cell.isFilled = True
    #         else:
    #             cell.isFilled = False

    #     rows = 8
    #     cols = 12


    #     for cell in cellList:
    #         row, col = cell.position # (0,0) first pass
    #         cell.h = 0

    #         for r in range(row-1, -1 , -1):
    #             above_cell = next((c for c in cellList if c.position == (r,col)), None)
    #             if above_cell and above_cell.isFilled:
    #                 cell.h += 1
    #         print(cell.position, cell.h, cell.isFilled)


    # #print(totalForEachGrid(my_ship, cells))
        


    
    # #totalForEachGrid(my_ship, cells)
    
        
    # isBalanced = False #get value from isbalance
    # siftCellGrid, siftBufferGrid = cells, buffer
    # def sift(isBalanced, siftCellGrid, siftBufferGrid):
    #     if isBalanced:
    #         return 
        
    #     def print_grid(cellList):
    #         grid = [['0' for _ in range(4)] for _ in range(3)]
    #         for i, cell in enumerate(cellList):
    #             row, col = cell.position
    #             print("BUFFFER") 
    #             print_buffer(buffer)
    #             if cell.isFilled:
    #                 grid[row][col] = str(cell.container.weight)
    #         print("Grid:")
    #         for row in grid:
    #             print(' '.join(str(cell).ljust(2) for cell in row))  # Ensure proper alignment
    #         print()

    #     # Print buffer grid representation
    #     def print_buffer(siftBufferGrid):
    #         grid = [['0' for _ in range(4)] for _ in range(3)]  # 3x4 buffer grid
    #         for buff in siftBufferGrid:
    #             row, col = buff.position
    #             if buff.isFilled:
    #                 grid[row][col] = str(buff.container.weight)

    #         print("Buffer:")
    #         for row in grid:
    #             print(' '.join(str(cell).ljust(2) for cell in row))  # Ensure proper alignment
    #         print()
    #     def is_main_grid_full(cellList):
    #         return all(cell.isFilled for cell in cellList)
        
    #     def move_to_buffer(siftCellGrid, siftBufferGrid):
    #         # Get all filled cells, sorted by container weight (heaviest first)
    #         filled_cells = sorted(
    #             [cell for cell in siftCellGrid if cell.isFilled],
    #             key=lambda c: c.container.weight,
    #             reverse=True  # Sort in descending order
    #         )

    #         if not filled_cells:
    #             return False, siftCellGrid, siftBufferGrid  # No containers to move

    #         for cell in filled_cells:
    #             # Find an empty buffer slot for the container
    #             empty_buffer_slot = next((buff for buff in siftBufferGrid if not buff.isFilled), None)
                
    #             if empty_buffer_slot:
    #                 # Move the container to the buffer
    #                 empty_buffer_slot.container = cell.container
    #                 empty_buffer_slot.isFilled = True
    #                 cell.isFilled = False
    #                 cell.container = None  # Clear the cell
    #                 print(f"Moved container from {cell.position} to buffer at {empty_buffer_slot.position}")
    #             else:
    #                 # No more empty buffer slots available
    #                 break

    #         return True, siftCellGrid, siftBufferGrid  # Return updated grids

        
        
        
    #     # def move_from_buffer(siftCellGrid, siftBufferGrid):
    #     #     filled_buffers = [buff for buff in siftBufferGrid if buff.isFilled]
            
    #     #     if not filled_buffers:
    #     #         return False  # No containers to move

    #     #     for buff in filled_buffers:
    #     #         empty_cell = next((cell for cell in siftCellGrid if not cell.isFilled), None)
                
    #     #         if empty_cell:
    #     #             empty_cell.container = buff.container
    #     #             empty_cell.isFilled = True
    #     #             buff.isFilled = False
    #     #             buff.container = None  # Clear the buffer slot
    #     #             print(f"Moved container {buff.container} from buffer at {buff.position} to grid at {empty_cell.position}")

    #         return True      
        
    #     def move_from_buffer(siftCellGrid, siftBufferGrid):
    
    #         filled_buffers = [buff for buff in siftBufferGrid if buff.isFilled]

    #         if not filled_buffers:
    #             return False  # No containers to move

    #         # Step 2: Sort containers by weight (heaviest to lightest)
    #         sorted_buffers = sorted(
    #             filled_buffers, 
    #             key=lambda b: b.container.weight, 
    #             reverse=True
    #         )

    #         # Step 3: Define the filling order for the grid (center-first strategy)
    #         fill_order = []
    #         row,col= 3,4
    #         mid=math.floor((col-1)/2)
    #         for i in range(row):
    #             fill_order.append((i,mid))
    #             for j in range(1, mid+1):
    #                 fill_order.append((i,mid+j))
    #                 fill_order.append((i,mid-j))
    #             fill_order.append((i,mid+j+1))


    #         for i, pos in enumerate(fill_order):
    #             if i < len(sorted_buffers):  
    #                 buffer_slot = sorted_buffers[i]
    #                 target_cell = next(
    #                     (cell for cell in siftCellGrid if cell.position == pos and not cell.isFilled), 
    #                     None
    #                 )
    #                 if target_cell:
    #                     target_cell.container = buffer_slot.container
    #                     target_cell.isFilled = True
    #                     buffer_slot.isFilled = False
    #                     buffer_slot.container = None  
    #                     print(f"Moved container {target_cell.container} to grid at {target_cell.position}")

    #         return True
        
     

    #     if move_to_buffer(siftCellGrid, siftBufferGrid):
    #         print_grid(siftCellGrid)  # Print grid after moving to buffer
    #         print_buffer(buffer)  # Print buffer state after moving containers
    #     else:
    #         return  # No more room in the buffer

    #     print("AFTER")

           
    #     if move_from_buffer(siftCellGrid, siftBufferGrid):
    #         print_grid(siftCellGrid)  # Print grid after moving from buffer
    #         print_buffer(buffer)  # Print buffer state after moving containers



    #     print_buffer(buffer)
    #     return True
        
    # def apply_gravity(cellList):
    #     columns = 12  # Number of columns in your grid
    #     rows = 8      # Number of rows in your grid
        
    #     # Process each column
    #     for col in range(1, columns + 1):
    #         # Start from the bottom row
    #         for bottom_row in range(rows, 1, -1):
    #             if not any(cell.isFilled and cell.position == (bottom_row, col) for cell in cellList):
    #                 # Found an empty space, look for container above to drop down
    #                 for top_row in range(bottom_row - 1, 0, -1):
    #                     above_cell = next((cell for cell in cellList if cell.position == (top_row, col) and cell.isFilled), None)
    #                     if above_cell:
    #                         # Found a container above, move it down
    #                         bottom_cell = next(cell for cell in cellList if cell.position == (bottom_row, col))
                            
    #                         # Swap containers
    #                         bottom_cell.container = above_cell.container
    #                         bottom_cell.isFilled = True
    #                         above_cell.container = Container("UNUSED", 0)
    #                         above_cell.isFilled = False
    #                         break


    # # print(sift(isBalanced, siftCellGrid, siftBufferGrid))
    # print( totalForEachGrid(my_ship, cells))

    # if balanceContainers(my_ship, cells, buffer):
        
    #     print("Balanced")
    # else:
    #     print("Not Blaanced")
    


    # def printBalanceMatrix():
    #     matrix = np.zeros((3, my_ship.columns), dtype=int)
        
    #     for position, container in my_ship.shipDict.items():
    #         row, col = position
    #         matrix[row, col] = container.weight
        
    #     print("Balance Matrix:")
    #     print(matrix)
        
    #     left_total = np.sum(matrix[:, [0,1]])
    #     right_total = np.sum(matrix[:, [2,3]])

     

    #     total_weight = left_total + right_total
        
    #     percentage_difference = abs(left_total - right_total) / total_weight * 100
        
    #     print(f"\nLeft Total: {left_total}")
    #     print(f"Right Total: {right_total}")
    #     print(f"Percentage Difference: {percentage_difference:.2f}%")



    #printOriginalMatrix()
    
    #balanceContainers(my_ship, cells)
    
    #printBalanceMatrix()


    my_ship.displayContainers()

if __name__ == "__main__":
    main()


def apply_gravity(cellList):
    columns = 12  # Number of columns in your grid
    rows = 8      # Number of rows in your grid
    
    # Process each column
    for col in range(1, columns + 1):
        # Start from the bottom row
        for bottom_row in range(rows, 1, -1):
            if not any(cell.isFilled and cell.position == (bottom_row, col) for cell in cellList):
                # Found an empty space, look for container above to drop down
                for top_row in range(bottom_row - 1, 0, -1):
                    above_cell = next((cell for cell in cellList if cell.position == (top_row, col) and cell.isFilled), None)
                    if above_cell:
                        # Found a container above, move it down
                        bottom_cell = next(cell for cell in cellList if cell.position == (bottom_row, col))
                        
                        # Swap containers
                        bottom_cell.container = above_cell.container
                        bottom_cell.isFilled = True
                        above_cell.container = Container("UNUSED", 0)
                        above_cell.isFilled = False
                        break

