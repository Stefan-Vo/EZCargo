def unload(shipDict, start, end):
    """
    Unloads a container from the ship to the truck.

    Args:
        shipDict (dict): Dictionary representing the ship grid.
        start (tuple): Starting position of the container on the ship grid.
        end (tuple): Target position (e.g., on the truck).

    Returns:
        list: Shortest path coordinates from start to end.
    """
    # Validate inputs
    if start not in shipDict:
        raise ValueError("Invalid start position on the ship grid")
    if shipDict[start] is None:
        raise ValueError("No container at the start position on the ship")

    # Simulate target position on the truck (not part of shipDict)
    shipDict[end] = None  # Temporary setup for the truck grid

    # Find the shortest path using A*
    path = find_shortest_path_a_star(shipDict, start, end)

    if not path:
        print("No path found")
        return []

    # Move the container along the path
    container = shipDict[start]
    for step in path[:-1]:  # Clear intermediate steps
        shipDict[step] = None
    shipDict[end] = container  # Place the container at the truck
    shipDict[start] = None  # Clear the ship position

    return path
