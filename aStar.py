import heapq

def find_shortest_path_a_star(shipDict, start, end):
    """
    A* algorithm to find the shortest path in the ship grid.

    Args:
        shipDict (dict): Dictionary representing the ship grid.
        start (tuple): Starting position (row, column).
        end (tuple): Target position (row, column).

    Returns:
        list: List of coordinates representing the shortest path, or an empty list if no path exists.
    """
    def heuristic(a, b):
        # Manhattan distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

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
        for drow, dcol in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
            neighbor = (current[0] + drow, current[1] + dcol)

            # Skip invalid or occupied cells
            if neighbor not in shipDict or (neighbor != end and shipDict[neighbor] is not None):
                continue

            # Calculate new g_cost for the neighbor
            new_g = g_cost[current] + 1  # Cost of moving to a neighbor is 1
            if neighbor not in g_cost or new_g < g_cost[neighbor]:
                g_cost[neighbor] = new_g
                f_cost = new_g + heuristic(neighbor, end)
                heapq.heappush(pq, (f_cost, neighbor))
                came_from[neighbor] = current

    return []  # No path found
