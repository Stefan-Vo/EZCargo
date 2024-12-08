import aStar;

def unload(shipDict, start, end):
    """
    Finds the paths to unload a container from the ship to the truck, handling blocking containers.

    Args:
        shipDict (dict): Dictionary representing the ship grid.
        start (tuple): Starting position of the target container on the ship grid.
        end (tuple): Target position (e.g., on the truck).

    Returns:
        list: A list of paths where each path corresponds to a container's movement.
    """
    if start not in shipDict:
        raise ValueError("Invalid start position on the ship grid")
    if shipDict[start] is None:
        raise ValueError("No container at the start position on the ship")

    # Step 1: Identify blocking containers
    blocking_containers = []
    for row in range(start[0] - 1, -1, -1):  # Iterate rows above the target
        position = (row, start[1])
        if shipDict.get(position):  # If there's a container at this position
            blocking_containers.append(position)

    # Step 2: Find paths to move blocking containers
    paths = []
    temp_shipDict = shipDict.copy()
    for block_position in blocking_containers:
        # Find the closest empty cell
        empty_cells = [pos for pos, value in temp_shipDict.items() if value is None]
        if not empty_cells:
            raise ValueError("No empty cells available to move blocking containers")

        closest_empty = min(empty_cells, key=lambda cell: abs(block_position[0] - cell[0]) + abs(block_position[1] - cell[1]))
        
        # Find path to move the blocking container
        path = aStar.find_shortest_path_a_star(temp_shipDict, block_position, closest_empty)
        if not path:
            raise ValueError(f"No path found to move blocking container at {block_position}")

        # Update the temporary ship grid
        temp_shipDict[block_position] = None
        temp_shipDict[closest_empty] = shipDict[block_position]

        # Add the path to the list of paths
        paths.append(path)

    # Step 3: Find path to move the target container
    target_path = aStar.find_shortest_path_a_star(temp_shipDict, start, end)
    if not target_path:
        raise ValueError("No path found to unload the target container")

    # Update the temporary ship grid for the target container
    temp_shipDict[start] = None
    temp_shipDict[end] = shipDict[start]

    # Add the target container's path to the list of paths
    paths.append(target_path)

    return paths
