from repository.image_repository import ImageRepository # Repository of images as base 64
from exceptions.exception import * # All the Exception Classes
from battleship.fleet import Fleet
from battleship.ships import Ship

'''*****************************************************************
 Class Player
	- Manages the player's fleet of ships
	- Manages the player's board arangement
*****************************************************************'''
class Player:
	
	BOARD_SIZE = 10
	
	def __init__(self):
		# Init a blank board (2D array of images as a base64)
		self._board = [[ImageRepository.get_empty_image() for col in range(Player.BOARD_SIZE)] for row in range(Player.BOARD_SIZE)]
	   
		self._fleet = Fleet() # Fleet of ships initialized
		
	def get_board(self):
		return self._board
	
	def get_fleet(self):
		return self._fleet.get_ships()
	
	'''*************************************************************
		Action Methods:
	*************************************************************'''
	def finish_board_placement(self):
		return self._fleet.is_valid_fleet()
	
	def place_ship(self, new_ship, flag):
		try:
			replaced_coords = self._fleet.add_ship(new_ship) # if return None: Did not replace. 
			if replaced_coords != None:
				for coord in replaced_coords:
					self._board[coord[0]][coord[1]] = ImageRepository.get_empty_image()
			if not flag:
				for position in new_ship.get_coord():
					self._board[position[0]][position[1]] = new_ship.get_token()
			return True	
		except (InvalidShipPlacementException, ShipAlreadyExistsException) as ex:
			print("exception thrown, halt program :" + str(ex) ) # Temporary action. 
			return False
 	
	# Returns True if this player lost. (GAME OVER)	
	def defend(self, coords): # THIS IS IF THE ENEMY OF THIS CURRENT OBJECT IS FIRING. 
		if self._board[coords[0]][coords[1]] == ImageRepository.get_hit_image() or self._board[coords[0]][coords[1]] == ImageRepository.get_miss_image():
			raise AlreadyPointTakenException("(other) player has already attempted an attack on this (row,col) point")
		elif self._fleet.check_for_damage(coords): # If the hit is taken, change the board image at current position to an X (hit)
			self._board[coords[0]][coords[1]] = ImageRepository.get_hit_image()
		else: # If the hit was not taken, change the board image at current position to an O (miss)
			self._board[coords[0]][coords[1]] = ImageRepository.get_miss_image()
		
		return self._fleet.is_empty() # returns true if CURRENT object lost