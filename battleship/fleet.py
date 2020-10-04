from battleship.ships import Ship

# Thrown if a ship's coordinates are not valid
class InvalidShipPlacementException(Exception):
	pass

# Thrown if a ship already exists within the fleet	
class ShipAlreadyExistsException(Exception):
	pass

class Fleet:
	
	def __init__(self):
		self.ships = [] # List of Ship objects
		
	def get_ships(self):
		return self.ships
		
	def get_ship_at(self, index):
		return self.ships[index]
	
	'''***********************************************************************
		add_ship(new_ship):
		- Throws exception if ship already exists on the ships list
		- Throws exception if a different type of ship already exists @ location on the board
		- Replaces previous placement of ship if new_ship is of the same type. 
	***********************************************************************'''
	def add_ship(self, new_ship): 
		if new_ship not in self.ships: # if exact type of ship not in fleet
			coords = new_ship.get_coord()
			for ship in self.ships:
				if ship.get_name() == new_ship.get_name(): # if adding a ship type that was already added (ex: another Carrier)
					ship = new_ship # Replace previous placement of ship
					break
				elif ship.is_already_placed(coords):
					raise InvalidShipPlacementException("Ship already exists at given coordinates")
			
			self.ships.append(new_ship) # Does not already exist on the fleet. Added to the fleet
		else:
			raise ShipAlreadyExistsException("Already added/duplicate request")
	
	def is_valid_fleet(self): # There MUST be 5 ships on the fleet otherwise, not a valid fleet. 
		print(len(self.ships))
		return len(self.ships) == 5
		
	
	'''****************************************************************
		Action Methods:
	****************************************************************'''
	def check_for_damage(self, coords):
		for ship in self.ships:
			if ship.hit(coords):
				return True
		return False