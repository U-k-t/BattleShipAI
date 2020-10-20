from exceptions.exception import * # All the Exception Classes
from repository.image_repository import ImageRepository # Repository of images as base 64

'''*****************************************************************
Class Ship:
	- Parent class of 5 distinct ships. 
	- Abstract
	
	Why different classes?
		- Only allows 5 different types of ships
		- flexibility if we are to add ship specific functions/actions
		- readability, adding ships with the class name of the ship readable. 
*****************************************************************'''
# Change the below to change the size of each ship
PATROL_SIZE = 2	   
SUB_SIZE = 3
DESTROY_SIZE = 3
BATTLE_SIZE = 4
CARRIER_SIZE = 5

class Ship():
	
	def __init__(self): # Creation of a non valid ship :
		self.size = -1
		self.name = " "
		self.coordinates = [] # Location points (List of tuples)
	
	def __init__(self, start, end, size, name): # Called only in child	  
		self.size = size
		self.name = name
		if self.__validate_coords(start, end) :
			self.coordinates = []
			self.__init_coordinates(start, end) # init list of coordinates				 
		else: #Excpetion must be caught upon ship creation
			raise InvalidShipException("invalid coordinates " + str(start) + " " + str(end)) 
	
	def get_coord(self):
		return self.coordinates
	
	def get_size(self):
		return self.size
		
	def get_name(self):
		return self.name
		
	def get_token(self):
		pass
	
	def __validate_coords(self, start, end): # Makes sure given coordinates for a ship are valid coordinates
		# DIAGONAL PLACEMENT NOT ALLOWED
		if(start[0] == end[0]):
			return ( abs(start[1] - end[1])+1 == self.get_size() )
		elif (start[1] == end[1]):
			return ( abs(start[0] - end[0])+1 == self.get_size() )
		return False # Given coordinates are NOT valid
	
	def __init_coordinates(self, start, end): # start/end tuple coordinates
		if (start[0] == end[0]):
			for y in range (start[1], end[1]+1):
				self.coordinates.append((start[0],y))
		else:
			for x in range (start[0], end[0]+1):
				self.coordinates.append((x,start[1]))
				

	'''***********************
		Action Methods:
	***********************'''
	
	def is_already_placed(self, compare_coords):
		for coord in compare_coords:
			if coord in self.coordinates:
				return True
		return False
	
	def hit(self, target): # target represents a tuple (row,col)
		if	target in self.coordinates :
			self.coordinates.remove(target)
			return True # successful hit
		return False
		
	def has_sunk(self):
		return self.coordinates is None or len(self.coordinates) == 0 # Returns True if the ship has been sunk ( No coordinates left)

class Patrol(Ship):
	
	def __init__(self, start, end):
		super().__init__(start, end, PATROL_SIZE, "Patrol")
	
	def get_token(self):
		return ImageRepository.get_patrol_token_image()

class Submarine(Ship):

	def __init__(self, start, end):
		super().__init__(start, end, SUB_SIZE, "Submarine")

	def get_token(self):
		return ImageRepository.get_submarine_token_image()
		
class Destroyer(Ship):

	def __init__(self, start, end):
		super().__init__(start, end, DESTROY_SIZE, "Destroyer")

	def get_token(self):
		return ImageRepository.get_destroyer_token_image()
	
class Battleship(Ship):

	def __init__(self, start, end):
		super().__init__(start, end, BATTLE_SIZE, "BattleShip")

	def get_token(self):
		return ImageRepository.get_battleship_token_image()
		
class Carrier(Ship):

	def __init__(self, start, end):
		super().__init__(start, end, CARRIER_SIZE, "Carrier")
		
	def get_token(self):
		return ImageRepository.get_carrier_token_image()