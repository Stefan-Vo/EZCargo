from ship import Ship
from container import Container
from operations import load_unload, balance_ship
from logger import Logger

def main():
    ship = Ship()
    logger = Logger("logfile.txt")

    load_unload(ship, to_unload=["C1", "C2"], to_load=[Container("C3", 500)])
    balance_ship(ship)

    logger.log("Load and balance operations completed")

if __name__ == "__main__":
    main()
