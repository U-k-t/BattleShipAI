from exceptions.exception import * # All the Exception Classes
from player import Player
from battleship.fleet import Fleet
from battleship.ships import *

import random

'''TODO: Implement '''

 # We can inherit from this to make a Butts / Butts Basic potentially 
class AI(Player):
	
	def __init__(self):
		super().__init__()
	
	def create_board(self):
		patrol = Patrol((0,0), (1,0))
		submarine = Submarine((2,3), (2,5))
		destroyer = Destroyer((4,8), (6,8))
		battleship = Battleship((6,2), (6,5))
		carrier = Carrier((8,1), (8,5))
		
		super().place_ship(patrol, True)
		super().place_ship(submarine, True)
		super().place_ship(destroyer, True)
		super().place_ship(battleship, True)
		super().place_ship(carrier, True)
	
	
	# THIS IS RANDOM TARGET FOR TESTING 
	# ToDo: Implement
	def give_target(self):
		return (random.randint(0, 9), random.randint(0,9))