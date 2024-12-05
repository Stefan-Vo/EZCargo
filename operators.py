from ship import ship
from container import Container
def load(ship, to_unload, to_load):
    pass

def unload(ship, to_unload, to_load):
    pass
myContainer = Container("Apple",500)
myContainer2 = Container("Apple2",300)
myContainer3 = Container("Apple3",500)
myContainer4 = Container("Apple4",300)
myContainer5 = Container("Apple5",900)
myContainer6 = Container("NAN",0)
myShip = ship([[[1,1],
[1,2],
[1,3],
[1,4]],
[[2,1],
[2,2],
[2,3],
[2,4]]])
myShip.addContainers((0,0),myContainer.getattr())
myShip.addContainers((0,1),myContainer2.getattr())
myShip.addContainers((0,2),myContainer.getattr())
myShip.addContainers((0,3),myContainer5.getattr())
myShip.addContainers((1,0),myContainer3.getattr())
myShip.addContainers((1,1),myContainer4.getattr())
myShip.addContainers((1,2),myContainer4.getattr())
myShip.addContainers((1,3),myContainer5.getattr())
myShip.addContainers((2,0),myContainer2.getattr())
myShip.addContainers((2,1),myContainer3.getattr())
myShip.addContainers((2,2),myContainer5.getattr())
myShip.addContainers((2,3),myContainer3.getattr())
myShip.addContainers((3,0),myContainer5.getattr())
myShip.addContainers((3,1),myContainer6.getattr())
myShip.addContainers((3,2),myContainer5.getattr())
myShip.addContainers((3,3),myContainer5.getattr())
def find_balance(ship):
    leftWeight = rightWeight = 0
    for row in range(3):
        for column in range(2):
            print(ship.shipDict[(row, column)][1])
            leftWeight += ship.shipDict[(row, column)][1]
    for row in range(3):
        for column in range(2,4):
            rightWeight += ship.shipDict[(row, column)][1]
    return leftWeight, rightWeight
            
def is_movable(ship, index):
    if index[0] == 3:
        return True
    print(index)
    if myShip.shipDict[(index[0]+1),index[1]][0] == "UNUSED" or myShip.shipDict[(index[0]+1),index[1]][0] == "NAN":
        print(myShip.shipDict[(index[0]),index[1]][0])
        return True
    return False

def move_to_right(ship,index):
    pass



def balance_ship(ship):
    pass
    leftWeight, rightWeight = find_balance(ship)
    if leftWeight - rightWeight == 0:
        return ship
    elif abs(leftWeight-rightWeight) <= .1*rightWeight:
        return ship
    balanced = False
    max_iter = 10000
    iter = 0
    copyShip = ship
    #while balanced == False and iter < max_iter:
    #for i in range(3):
    for row in range(4):
        for column in range(2):
            if is_movable(ship, [row,column]):
                print(row,column, "movable")
                move_to_right(copyShip,[row,column])


    



#print(find_balance(myShip))
print(balance_ship(myShip))