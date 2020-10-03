class Fleet:
    def __init__ (self):
        self.ships = {}
        self.fleetSize = 0

    def getShips(self):
        return self.ships

    def addShip(self,start,stop,ship):
        if (start[0] == stop[0]):
            for y in range (start[1], stop[1]+1):
                self.ships[(start[0],y)] = ship
        else:
            for x in range (start[0],stop[0]+1):
                self.ships[(x,start[1])] = ship
        self.fleetSize +=1
        return self.fleetSize

    def findPlacements(self,start,size):
        possible = []
        isViableX = True
        isViableY = True
        for x in range(1-size,size):
            if ((start[0]+x,start[1]) in self.ships):
                isViableX = False
            if ((start[0],start[1]+x) in self.ships):
                isViableY = False
            if x == 0 or x== size-1:
                if isViableX:
                    possible.append((start[0]-size+1 if x==0 else start[0]+size-1,start[1]))
                if isViableY:
                    possible.append((start[0],start[1]-size+1 if x==0 else start[1]+size-1))
                isViableX = True
                isViableY = True
        print(possible)
        return(possible)



class Ship (Fleet):
  def __init__ (self, size, name):
      self.size = size
      self.name = name
      self.units = [1 for x in range(size)]

  def getSize(self):
      return self.size
  def getName(self):
      return self.name
  def getUnits(self):
      return len(self.units)

  def hit(self):
      self.units.pop()
      return (len(self.units) == 0) # Returns True if the ship has been sunk

class Grid():
    def __init__(self):
        # self.board = [[str(row)+" "]+["  " for col in range (10)] for row in range(1,11)]
        # self.board.append(["  ", '1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10'])
        self.board = [["  " for col in range (10)] for row in range(10)]
        # self.board[9][0]="10"

    def getGrid(self):
        return self.board

    def setFleet(self, fleet):
        for key in fleet:
            self.board[key[1]][key[0]] = fleet[key].getName()[0] + " "

    def setPossible(self,possible):
        for coord in possible:
            if (coord[1] >=0 and coord[1]<=9) and (coord[0] >=0 and coord[0]<=9):
                self.board[coord[1]][coord[0]] = coord
    def clearPossible(self,possible):
        for coord in possible:
            if (coord[1] >=0 and coord[1]<=9) and (coord[0] >=0 and coord[0]<=9):
                self.board[coord[1]][coord[0]] = "  "

    def fire(self,coords,fleet):
        position = self.board[coords[1]][coords[0]]
        ships = fleet.getShips()
        if position == "X ":
            print("You already tried that one; it's a hit!")
            return True
        elif position != "  " and position != "O ":
            self.board[coords[1]][coords[0]] = "X "
            print("Hit!")
            ships[coords].hit()
            return True
        else:
            self.board[coords[1]][coords[0]] = "O "
            print("Miss!")
            return False

# def main():
#         player1 = Grid()
#         player1Opp = Grid()
#         Opp = Grid()
#         fleet = Fleet()
#         fleet.addShip((1,1),(1,2),Ship(2,"Patrol"))
#         fleet.addShip((2,1),(2,3),Ship(3,"Submarine"))
#         fleet.addShip((3,1),(3,3),Ship(3,"Destroyer"))
#         fleet.addShip((4,1),(4,4),Ship(4,"Battleship"))
#         fleet.addShip((5,1),(5,5),Ship(5,"Carrier"))
#         player1.setFleet(fleet.getShips())
#
#         while(True):
#             for row in player1.getGrid():
#                 print(row)
#             coords = eval(input("Target? (x,y): "))
#             player1.fire(coords,fleet)

            ## Below is Code for Setting Ships

            # possible = fleet.findPlacements(coords,2) # 2 Needs to be Variable Size
            # player1.setPossible(possible)
            # for row in player1.getGrid():
            #     print(row)
            # stopCoords =  input("Stop?: ")
            # fleet.addShip(coords,eval(stopCoords),Ship(2,"Kathryn"))
            # player1.clearPossible(possible)
            #
            # player1.setFleet(fleet.getShips())
