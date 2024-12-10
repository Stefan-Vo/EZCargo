import heapq
from copy import deepcopy

class Container:
    def __init__(self, weight):
        self.weight = weight

class Cell:
    def __init__(self, position):
        self.position = position
        self.container = None
    
    @property
    def isFilled(self):
        return self.container is not None
    
    @property
    def weight(self):
        return self.container.weight if self.container else 0
    
    def __lt__(self, other):
        # Compare cells based on position or other criteria
        return self.position < other.position

class Ship:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.grid = self._create_grid()
    
    def _create_grid(self):
        return [[Cell((row, col)) for col in range(self.columns)] for row in range(self.rows)]
    
    def place_container(self, row, col, container):
        """Place a container at a specific grid location"""
        self.grid[row][col].container = container
    
    def balance_containers(self):
        """Main method to balance containers across the ship"""
        # Convert grid to a flat list of cells for easier manipulation
        cell_list = [cell for row in self.grid for cell in row]
        mid = self.columns // 2
        
        def compute_weights():
            """Compute weights for left and right sides of the ship"""
            mid = self.columns // 2  # Integer division to find midpoint
            left_weight = sum(
                cell.weight for cell in cell_list 
                if cell.isFilled and cell.position[1] < mid
            )
            right_weight = sum(
                cell.weight for cell in cell_list 
                if cell.isFilled and cell.position[1] >= mid
            )
            return left_weight, right_weight
        
        def print_grid(current_grid):
            """Print the current state of the grid"""
            print("Grid:")
            for row in current_grid:
                print(' '.join(str(cell.weight) if cell.isFilled else '0' for cell in row))
            print()
        
        def total_weight():
            """Compute total weight of all containers"""
            return sum(cell.weight for cell in cell_list if cell.isFilled)
        
        def compute_heuristic(left_weight, right_weight, initial_total_weight):
            """Compute a numeric heuristic cost based on weight difference"""
            weight_diff = abs(left_weight - right_weight)
            balance_ratio = weight_diff / initial_total_weight
            return balance_ratio
        
        # Initial weight check
        initial_total_weight = total_weight()
        initial_left_weight, initial_right_weight = compute_weights()
        
        # Tracking for A* search
        open_set = []
        initial_state = (
            compute_heuristic(initial_left_weight, initial_right_weight, initial_total_weight),
            (deepcopy(self.grid), initial_left_weight, initial_right_weight, [])
        )
        heapq.heappush(open_set, initial_state)
        closed_set = set()
        
        while open_set:
            _, (current_grid, curr_left_weight, curr_right_weight, path) = heapq.heappop(open_set)
            
            # Check if balanced
            if abs(curr_left_weight - curr_right_weight) <= 0.1 * initial_total_weight:
                print("Balanced!")
                print(f"Left Weight: {curr_left_weight}, Right Weight: {curr_right_weight}")
                
                # Print optimal path
                print("\nOptimal Path:")
                for i, grid_state in enumerate(path + [current_grid]):
                    print(f"Step {i}:")
                    print_grid(grid_state)
                
                return True
            
            # Create a state key to avoid revisiting
            state_key = tuple(
                (cell.position, cell.isFilled, cell.weight) for row in current_grid for cell in row
            )
            if state_key in closed_set:
                continue
            closed_set.add(state_key)
            
            # Try moving each container
            for row in range(self.rows):
                for col in range(self.columns):
                    current_cell = current_grid[row][col]
                    
                    # Skip empty cells or cells with containers below
                    if not current_cell.isFilled:
                        continue
                    if any(
                        current_grid[r][col].isFilled 
                        for r in range(row + 1, self.rows)
                    ):
                        continue
                    
                    # Try moving to each other column
                    for target_col in range(self.columns):
                        if target_col == col:
                            continue
                        
                        # Find next empty row in target column
                        target_row = next(
                            (r for r in range(self.rows)  # Start from row 0 to self.rows - 1
                            if not current_grid[r][target_col].isFilled),
                            None  # Return None if no empty row is found
                        )
                        
                        if target_row is None:
                            continue
                        
                        # Create a new grid state with the move
                        new_grid = deepcopy(current_grid)
                        
                        # Move the container
                        container = new_grid[row][col].container
                        new_grid[row][col].container = None
                        new_grid[target_row][target_col].container = container
                        

                        # Compute new weights
                        if col < mid:
                            new_left_weight = curr_left_weight - current_cell.weight
                            new_right_weight = curr_right_weight + current_cell.weight
                        else:
                            new_left_weight = curr_left_weight + current_cell.weight
                            new_right_weight = curr_right_weight - current_cell.weight
                        
                        # Compute heuristic cost
                        h_cost = compute_heuristic(new_left_weight, new_right_weight, initial_total_weight)
                        
                        # Add to exploration set
                        new_path = path + [current_grid]
                        heapq.heappush(open_set, (h_cost, (new_grid, new_left_weight, new_right_weight, new_path)))
        
        print("No solution found to balance the ship.")
        return False

# Example usage
def main():
    # Create a ship with 3 rows and 4 columns
    ship = Ship(3, 4)
    
    # Place some containers
    ship.place_container(0, 0, Container(8))
    ship.place_container(0, 1, Container(7))
    ship.place_container(0, 2, Container(0))
    ship.place_container(0, 3, Container(0))
    ship.place_container(1, 0, Container(0))
    ship.place_container(1, 1, Container(0))
    ship.place_container(2, 1, Container(0))
    
    # Try to balance the ship
    ship.balance_containers()

if __name__ == "__main__":
    main()