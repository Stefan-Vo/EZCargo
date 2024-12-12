from ship import ship
from container import Container
#from operations import load_unload, balance_ship
from logger import Logger
from load import load
import numpy as np

def main():

    ship_matrix = np.zeros((3, 4), dtype=int) 
    ship2 = ship(ship_matrix)

    containers = [
        Container("S", 0),  # Container A with weight 10
        Container("A", 5)]
    positions = [(0, 0), (0, 1), (0, 2), (0, 3), 
                 (1, 0), (1, 1), (1, 2), (1, 3),
                 (2, 0), (2, 1), (2, 2), (2, 3)]
    for container, position in zip(containers, positions):
        ship2.addContainers(position, container)
    
    logger = Logger("logfile.txt")
    container = Container("obamna", 5)

    
    load(ship2, tuple((0,0)), container)

    # load_unload(ship, to_unload=["C1", "C2"], to_load=[Container("C3", 500)])
    # balance_ship(ship)

    # logger.log("Load and balance operations completed")

if __name__ == "__main__":
    main()
