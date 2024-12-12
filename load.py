import aStar;

def load(shipDict, start, container):
    """
    Finds the shortest path to load a container from the truck to the closest empty cell on the ship.

    Args:
        shipDict (dict): Dictionary representing the ship grid.
        start (tuple): Starting position of the container (e.g., on the truck).
        container (tuple): The container data as (container_id, weight).

    Returns:
        tuple: (path, destination) where:
            - path (list): Shortest path coordinates from start to destination.
            - destination (tuple): The chosen destination cell.
    """
    # Find all empty cells

    empty_cells = [pos for pos, value in shipDict.shipDict.items() if value is None]

    if not empty_cells:
        raise ValueError("No empty cells available on the ship")

    # Find the closest empty cell based on Manhattan distance
    closest_cell = min(empty_cells, key=lambda cell: abs(start[0] - cell[0]) + abs(start[1] - cell[1]))

    # Use A* to calculate the shortest path to the chosen destination
    temp_shipDict = shipDict.copy()
    temp_shipDict[start] = container  # Temporarily mark the truck position for pathfinding
    path = aStar.find_shortest_path_a_star(temp_shipDict, start, closest_cell)

    if not path:
        print("No path found to destination")
        return [], closest_cell

    return path, closest_cell
