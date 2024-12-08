import aStar;

def load(shipDict, start, end, container):
    """
    Loads a container from the truck to the ship.

    Args:
        shipDict (dict): Dictionary representing the ship grid.
        start (tuple): Starting position of the container (e.g., from the truck).
        end (tuple): Target position on the ship grid.
        container (tuple): The container data as (container_id, weight).

    Returns:
        list: Shortest path coordinates from start to end.
    """
    # Validate inputs
    if end not in shipDict:
        raise ValueError("Invalid end position on the ship grid")
    if shipDict[end] is not None:
        raise ValueError("Target position is not empty on the ship")

    # Simulate starting position on the truck (not part of shipDict)
    shipDict[start] = container  # Temporary placement on the truck grid

    # Find the shortest path using A*
    path = aStar.find_shortest_path_a_star(shipDict, start, end)

    if not path:
        print("No path found")
        shipDict[start] = None  # Clear temporary placement
        return []

    # Move the container along the path
    for step in path[:-1]:  # Clear intermediate steps
        shipDict[step] = None
    shipDict[end] = container  # Place the container at the destination
    shipDict[start] = None  # Clear the truck position

    return path
