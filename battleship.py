class Fleet:
    def __init__ (self):
        """
        Initializes a Fleet Class

        Parameters
        ----------
        self : Fleet Object

        Attributes
        -------
        ships : dict
            Dictinary in storing the positions of all ships in the fleet
            Stores the ships in format (x,y) : ship, where (x,y) is a tuple of integers representing a "peg" on the ship and ship is a Ship Object
        fleetSize: int
            Integer representing the number of ships added to the fleet
        """

        self.ships = {}
        self.fleetSize = 0

    def getShips(self):
        """
        Returns the dictionary of ships stored by the fleet

        Parameters
        ----------
        self : Fleet Object

        Returns
        -------
        self.ships : dict
            Dictinary in storing the positions of all ships in the fleet
            Stores the ships in format (x,y) : ship, where (x,y) is a tuple of integers representing a "peg" on the ship and ship is a Ship object
        """

        return self.ships

    def addShip(self,start,stop,ship):
        """
        Adds a ship object to the fleet

        Iterates over points between the start and stop of the ship to create dictionary keys that refer to the Ship object

        Parameters
        ----------
        self : Fleet Object
        start : tuple
            Tuple of integers in format (x,y) representing one end of the ship's position
        stop: tuple
            Tuple of integers in format (x,y) representing one end of the ship's position
        ship : Ship Object
            The ship being added to the fleet

        Returns
        -------
        self.fleetSize : int
            The number of ships in the fleet after adding the ship
        """

        if (start[0] == stop[0]):
            for y in range (start[1], stop[1]+1):
                self.ships[(start[0],y)] = ship
        else:
            for x in range (start[0],stop[0]+1):
                self.ships[(x,start[1])] = ship
        self.fleetSize +=1
        return self.fleetSize

    def findPlacements(self,start,size):
        """
        Finds valid endpoints for a ship based on its starting point and its size

        Ensures that ships don't overlap with one another by checking that a potential "peg" is not already represented as a dictionary key

        Parameters
        ----------
        self : Fleet Object
        start : tuple
            Tuple of integers in format (x,y) representing one end of the ship's position
        size : int
            The size of the ship being added

        Returns
        -------
        possible : list
            A list of integer tuples in format (x,y) of all valid potential endpoints of the ship
            0 <= len(possible) <= 4
        """

        possible = []
        isViableX = True
        isViableY = True
        for x in range(1-size,size):
            if ((start[0]+x,start[1]) in self.ships): # Checks for Valid Horizontal Positions
                isViableX = False
            if ((start[0],start[1]+x) in self.ships): # Checks for Valid Vertical Positions
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
      """
      Initializes a Ship Class

      Parameters
      ----------
      self : Ship Object
      size : int
        The number of grid units the ship occupies
      name : String
        The name of the ship

      Attributes
      -------
      size : int
          The number of grid units the ship occupies
      name : String
          The name of the ship
      units: list
        A list of integers; it's length represents the remaining number of times the ship can be hit.
      """

      self.size = size
      self.name = name
      self.units = [1 for x in range(size)]

  def getSize(self):
      """
      Returns the size of the ship

      Parameters
      ----------
      self : Ship Object

      Returns
      -------
      self.size : int
        The number of grid units the ship occupies
      """

      return self.size

  def getName(self):
      """
      Returns the name/type of the ship

      Parameters
      ----------
      self : Ship Object

      Returns
      -------
      self.name : String
        The name of the ship
      """

      return self.name

  def getUnits(self):
      """
      Returns the number of times the ship can be hit

      Parameters
      ----------
      self : Ship Object

      Returns
      -------
      len(self.units) : int
        The remaining number of times the ship can be hit
      """

      return len(self.units)

  def hit(self):
      """
      Simulates a sucessful "hit" action on the ship

      Removes an element from self.units

      Parameters
      ----------
      self : Ship Object

      Returns
      -------
      len(self.units) == 0 : Boolean
        Returns True if the ship has been sunk
      """

      self.units.pop()
      return (len(self.units) == 0) # Returns True if the ship has been sunk

class Grid():
    def __init__(self):
        """
        Initializes a Grid Class

        Parameters
        ----------
        self : Grid Object

        Attributes
        -------
        board : 2D list
            10x10 grid of "  " that mirrors the grid in the UI. Represents an empty grid.

        """

        # self.board = [[str(row)+" "]+["  " for col in range (10)] for row in range(1,11)]
        # self.board.append(["  ", '1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10'])
        self.board = [["  " for col in range (10)] for row in range(10)]
        # self.board[9][0]="10"

    def getGrid(self):
        """
        Returns the current Grid

        Parameters
        ----------
        self : Grid Object

        Returns
        -------
        self.board : list
            List of lists of strings representing the current state of the board
        """

        return self.board

    def setFleet(self, fleet):
        """
        Updates the grid with the position of all ships in the fleets

        Uses keys in the fleet to set the value of the string in the 2D array at the coordinates (key1,key0) to be the first initial of the Ship's name followed by a space

        Parameters
        ----------
        self : Grid Object
        fleet: dict
            Fleet.getShips() - dictionary with 2D-coordinates (tuples of ints)  as keys and ships as values
        """

        for key in fleet:
            self.board[key[1]][key[0]] = fleet[key].getName()[0] + " "

    def setPossible(self,possible):
        """
        Updates the grid with the position of all possible placements for a ship

        Validates that the coordinates are within the bounds of the board, then updates the position on the grid with a "? "

        Parameters
        ----------
        self : Grid Object
        possible: list
            list of integer tuples in format (x,y)
            generated using Fleet.findPlacements
        """
        
        for coord in possible:
            if (coord[1] >=0 and coord[1]<=9) and (coord[0] >=0 and coord[0]<=9): # Validate that position is within bounds
                self.board[coord[1]][coord[0]] = "? "

    def clearPossible(self,possible):
        """
        Removes the markers used to indicate possible valid placements for a ship

        Validates that the coordinates are within the bounds of the board, then updates the position on the grid with a "  "

        Parameters
        ----------
        self : Grid Object
        possible: list
            list of integer tuples in format (x,y)
            generated using Fleet.findPlacements
        """

        for coord in possible:
            if (coord[1] >=0 and coord[1]<=9) and (coord[0] >=0 and coord[0]<=9):
                self.board[coord[1]][coord[0]] = "  "

    def fire(self,coords,fleet):
        """
        Represents an action taken by a player selecting a set of coordinates
        Determines if the action results in a hit or miss and updates the grid accordingly

        Parameters
        ----------
        self : Grid Object
        coords : tuple
            Tuple of integers in format (x,y) representing a position on the grid
        fleet : Fleet Object
            The set of ships stored on the grid

        Returns
        -------
        : Boolean
            True if a ship resides on coords, false if it's a miss
        """

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
