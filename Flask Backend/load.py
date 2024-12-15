from copy import deepcopy
from ship import ship
from container import Container
#from operations import load_unload, balance_ship
from logger import Logger
# from load import load
import numpy as np
import heapq
import random

#-------------------------------------

def find_shortest_path_a_star(moveFrom, moveTo, start, end):
    """
    A* algorithm to find the shortest path in the ship grid, accounting for crane lifting.

    Args:
        moveFrom (dict or list): Source grid (e.g., buffer).
        moveTo (dict): Destination grid (e.g., ship).
        start (tuple): Starting position (row, column).
        end (tuple): Target position (row, column).

    Returns:
        list: List of coordinates representing the shortest path, or an empty list if no path exists.
    """
    def heuristic(a, b):
        # Manhattan distance
        return abs(a[0] + 5)+abs(b[0]+8) + abs(a[1]+24)+abs(12+ b[1]) + 4+2
    # Priority queue for A* (min-heap)
    pq = []
    heapq.heappush(pq, (0, start))  # (cost, current position)

    # Cost from start to current position
    g_cost = {start: 0}
    # Path tracking
    came_from = {}

    while pq:
        _, current = heapq.heappop(pq)

        # Check if we reached the goal
        if current == end:
            # Reconstruct the path
            path = []
            while current:
                path.append(current)
                current = came_from.get(current)
            return path[::-1]  # Reverse the path

        # Explore neighbors
        pmoves=[]
        if(len(moveTo)==96):
          r=8
          c=12
        else:
          r=4
          c=24
        for i in range(r):
          for j in range(c):
            pmoves.append((i,j))
        for i in range(r):
          for j in range(c):
            pmoves.append((-i,-j))
        # print(pmoves)
        for pmove in pmoves:
            # Check if the move is within bounds
            if pmove[0] < 0 or pmove[0] >= r or pmove[1] < 0 or pmove[1] >= c:
                continue

            # Allow crane to lift containers vertically:
            # Skip only if the target position is occupied (but not blocked by inaccessible rows).
            if pmove in moveTo and moveTo[pmove].id != "UNUSED" and pmove != end:
                continue
            # print(pmove)
            # Calculate new g_cost for the neighbor
            new_g = g_cost[current] + 1  # Cost of moving to a neighbor is 1
            if pmove not in g_cost or new_g < g_cost[pmove]:
                g_cost[pmove] = new_g
                f_cost = new_g + heuristic(pmove, end)
                heapq.heappush(pq, (f_cost, pmove))
                came_from[pmove] = current

    return []  # No path found


def load(shipDict, buffer_dict, start_list):
  for start in start_list:
      print("\n--- START LOAD FUNCTION ---")
      # Retrieve the container from the buffer at the start position
      print(f"Checking buffer at position {start}")
      if start not in buffer_dict:
          raise ValueError(f"Invalid start position: {start}")
      
      container = buffer_dict[start]
      if container.id == "UNUSED":
          raise ValueError(f"No valid container at buffer position {start}")

      print(f"Target container: ID={container.id}, Weight={container.weight}")

      # Find all valid empty cells on the ship
      empty_cells = []
      for pos,value in shipDict.shipDict.items():
        if value.id == "UNUSED":
              if pos[0] == 8 - 1 :
                empty_cells.append(pos) # On the ground
              elif pos[0] < 8- 1 and shipDict.shipDict[(pos[0] + 1, pos[1])].id != "UNUSED":
                empty_cells.append(pos) 

      if not empty_cells:
          print("Error: No valid empty cells available on the ship")
          return [], None

      print(f"Valid empty cells: {empty_cells}")

      # Find the closest empty cell based on Manhattan distance
      closest_cell = min(empty_cells, key=lambda cell: abs(start[0] + 5)+abs(cell[0]+8) + abs(start[1]+24)+abs(12 + cell[1]) + 4+2)
      print(f"Closest empty cell: {closest_cell}")

      # Use A* to calculate the shortest path to the chosen destination
      print("Running A* to find the shortest path...")
      temp_shipDict = deepcopy(shipDict)
      temp_shipDict.shipDict[start] = container  # Temporarily mark the buffer position for pathfinding
      path = find_shortest_path_a_star(buffer_dict, temp_shipDict.shipDict, start, closest_cell)
      

      if not path:
          print("No path found to destination.")
          return [], closest_cell

      # print(f"Calculated path: {path}")

      # Update the shipDict to reflect the container's new position
      shipDict.shipDict[closest_cell] = container
      # del shipDict.shipDict[start]  # Remove container from the original position in the shipDict

      # Update the buffer to reflect the container's removal
      buffer_dict[start] = Container("UNUSED", 0)  # Mark the buffer position as unused
      print(f"Successfully moved container to {closest_cell}")
      print("\n--- END LOAD FUNCTION ---\n")
  return buffer_dict, shipDict

def unload(shipDict, buffer_dict, start_list):
  for start in start_list:
      print("\n--- START UNLOAD FUNCTION ---")
      # Retrieve the container from the ship at the start position
      print(f"Checking ship at position {start}")
      if start not in shipDict.shipDict:
          raise ValueError(f"Invalid start position: {start}")
      
      container = shipDict.shipDict[start]
      print(start)
      if container.id == "UNUSED":
          raise ValueError(f"No valid container at ship position {start}")

      print(f"Target container: ID={container.id}, Weight={container.weight}")

      # Find all valid empty cells on the ship
      empty_cells = []
      for pos, value in buffer_dict.items():
          # print(buffer_dict[(pos[0] + 1, pos[1])].id)
          if value.id == "UNUSED":
              if pos[0] == 4 - 1 :
                empty_cells.append(pos) # On the ground
              elif pos[0] < 4- 1 and buffer_dict[(pos[0] + 1, pos[1])].id != "UNUSED":
                empty_cells.append(pos)  # Container below

      if not empty_cells:
          print("Error: No valid empty cells available on the buffer")
          return [], None

      print(f"Valid empty cells: {empty_cells}")

      # Find the closest empty cell based on Manhattan distance
      closest_cell = min(empty_cells, key=lambda cell: abs(start[0] - cell[0]) + abs(start[1] - cell[1]))
      print(f"Closest empty cell: {closest_cell}")

      # Use A* to calculate the shortest path to the chosen destination
      print("Running A* to find the shortest path...")
      temp_buffDict = deepcopy(buffer_dict)
      temp_buffDict[start] = container  # Temporarily mark the buffer position for pathfinding
      path = find_shortest_path_a_star(shipDict.shipDict, temp_buffDict, start, closest_cell)
      

      if not path:
          print("No path found to destination.")
          return [], closest_cell

      # print(f"Calculated path: {path}")

      # Update the shipDict to reflect the container's new position
      buffer_dict[closest_cell] = container
      # buffer_dict[start].id="UNUSED"
      # buffer_dict[start].weight=0 # Remove container from the original position in the shipDict

      # Update the buffer to reflect the container's removal
      shipDict.shipDict[start] = Container("UNUSED", 0)  # Mark the buffer position as unused
      print(f"Successfully moved container to {closest_cell}")
      print("\n--- END UNLOAD FUNCTION ---\n")
  return buffer_dict, shipDict
# SHIP
def reload_ship(ship):
    """
    Reload the ship with hardcoded containers, ensuring no floating containers.

    Args:
        ship (ship): The ship object to be reloaded.

    Returns:
        None
    """
    # Clear the shipDict for reloading
    ship.shipDict = {}

    # Define hardcoded containers with positions and weights
    hardcoded_containers = {
        
        # Fill other positions with "UNUSED"
    }

    # Add the hardcoded containers to the ship
    for position, container in hardcoded_containers.items():
        ship.addContainers(position, container)

    # Fill remaining positions with "UNUSED"
    rows, cols = ship.rows, ship.columns
    for row in range(8):
        for col in range(12):
            position = (row, col)
            if position not in ship.shipDict:
                ship.addContainers(position, Container("UNUSED", 0))


# Create a 3x4 ship grid
ship_matrix = [[0 for _ in range(12)] for _ in range(8)]
myShip = ship(ship_matrix)
# Reload the ship with hardcoded containers
reload_ship(myShip)


# myShip.displayContainers()

def display_ship_as_grid(ship):

    rows = ship.rows
    cols = ship.columns
    grid = [["0" for _ in range(12)] for _ in range(8)]  # Initialize a blank grid

    for position, container in ship.shipDict.items():
        row, col = position
        grid[row][col] = str(container.weight)  # Fill grid with container weights

    # Print the grid
    print("Ship:")
    for row in grid:
        print(' '.join(str(cell).ljust(3) for cell in row))  # Ensure proper alignment
    print()


# BUFFER
buffer_dict = {}
def printAndFillBuffer(rows=4, cols=24):
    """
    Creates a buffer as a dictionary (like shipDict), fills it with hardcoded containers, and prints it.

    Args:
        rows (int): Number of rows in the buffer grid.
        cols (int): Number of columns in the buffer grid.

    Returns:
        dict: The buffer grid as a dictionary, with positions as keys and containers as values.
    """
    

    # Hardcode specific containers into the buffer
    hardcoded_containers = {
        (1, 2): Container("Catfish",60),
        (1, 3): Container("Dogana", 20),
        (1, 4): Container("Batons", 20),
        (2,2): Container("Rations for US Army", 20)
        # Fill other positions with "UNUSED"
        # All other positions will be "UNUSED"
    }

    # Fill the buffer with hardcoded containers and "UNUSED" for empty spots
    for row in range(rows):
        for col in range(cols):
            position = (row, col)
            if position in hardcoded_containers:
                # Add a hardcoded container
                buffer_dict[position] = hardcoded_containers[position]
            else:
                # Fill other positions with "UNUSED"
                buffer_dict[position] = Container("UNUSED", 0)

    # Print the buffer grid
    print("Buffer:")
    for row in range(rows):
        row_data = []
        for col in range(cols):
            position = (row, col)
            container = buffer_dict[position]
            row_data.append(str(container.weight))
        print(' '.join(row_data))
    print()

    return buffer_dict

def main():
    """
    ship_matrix = np.zeros((3, 4), dtype=int)
    ship2 = ship(ship_matrix)
    # buff_matrix = np.zeros((3,4),dtype=int)

    containers = [
        Container("a", 20),
        Container("b", 5),
        Container("c", 0),
        Container("UNUSED", 0),
        Container("e", 0),
        Container("f", 0),
        Container("g", 5),
        Container("h", 0),
        Container("i", 0),
        Container("j", 0),
        Container("k", 0),
        Container("l", 0),]
    positions = [(0, 0), (0, 1), (0, 2), (0, 3),
                 (1, 0), (1, 1), (1, 2), (1, 3),
                 (2, 0), (2, 1), (2, 2), (2, 3)]
    for container, position in zip(containers, positions):
        ship2.addContainers(position, container)

    # logger = Logger("logfile.txt")

    container = Container("target", 5)
    """
    global myShip, buffer_dict
    start_position = (0, 0)
    printAndFillBuffer()
    display_ship_as_grid(myShip)
    start_list=[]
    start_list2=[]
    for i in buffer_dict:
      if(buffer_dict[i].id!="UNUSED"):
        start_list.append(i)

    for i in range(8):
      for j in range(12):
        if(myShip.shipDict[(i,j)].id!="UNUSED"):
          start_list2.append((i,j))
    print(start_list2)
    # for i in myShip.shipDict:
    #   print(i,myShip.shipDict[i].id)
    # myShip.matrix
    # buffer_dict.matrix
    buff,ship=load(myShip, buffer_dict, start_list)
    # buff,ship=unload(myShip, buffer_dict, start_list2)
    display_ship_as_grid(ship)
    
    
    # load()

    # load_unload(ship, to_unload=["C1", "C2"], to_load=[Container("C3", 500)])
    # balance_ship(ship)

    # logger.log("Load and balance operations completed")

if __name__ == "__main__":
    main()