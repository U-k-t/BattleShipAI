from exceptions.exception import * # All the Exception Classes
from players.player import Player
from players.database import Database
from battleship.fleet import Fleet
from battleship.ships import *


import random

'''TODO: Implement '''

 # We can inherit from this to make a Butts / Butts Basic potentially 
class AI(Player):
	
	def __init__(self):
		super().__init__()
	
	def create_board(self):
		self.place_patrol()
		self.place_submarine()
		self.place_destroyer()
		self.place_battleship()
		self.place_carrier()
	
	def place_patrol(self):
		while(True):
			start, end = self.make_ship(2)
			if(super().place_ship(Patrol(start, end),True)):
				print( "PLACED A PATROL AT " +str(start) + "," + str(end))
				return
		
	def place_submarine(self):
		while(True):
			start, end = self.make_ship(3)
			if(super().place_ship(Submarine(start, end),True)):
				print( "PLACED A SUBMARINE AT " +str(start) + "," + str(end))
				return
	
	def place_destroyer(self):
		while(True):
			start, end = self.make_ship(3)
			if(super().place_ship(Destroyer(start, end),True)):
				print( "PLACED A DESTROYER AT " +str(start) + "," + str(end))
				return
	
	def place_battleship(self):
		while(True):
			start, end = self.make_ship(4)
			if(super().place_ship(Battleship(start, end),True)):
				print( "PLACED A BATTLESHIP AT " +str(start) + "," + str(end))
				return
	
	def place_carrier(self):
		while(True):
			start, end = self.make_ship(5)
			if(super().place_ship(Carrier(start, end),True)):
				print( "PLACED A CARRIER AT " +str(start) + "," + str(end))
				return
	
	def make_ship(self,size):
		coin = random.randint(0, 1)				
		start = (random.randint(0, 9), random.randint(0,9))
		
		if coin == 0: #Horizontal Placement
			left = start[0] - (size - 1)
			right = start[0] + (size - 1)
			if left >= 0:
				if right <= 9:
					end = (random.choice([left,right]), start[1])
				else:
					end = (left, start[1])
			else:
				end = (right, start[1])					
		else: #Vertical Placement
			up = start[1] - (size - 1)
			down = start[1] + (size - 1)
			if up >= 0:
				if down <= 9:
					end = (start[0], random.choice([up,down]))
				else:
					end = (start[0], up)
			else:
				end = (start[0], down)
		return (start,end)
	
	
	# THIS IS RANDOM TARGET FOR TESTING 
	# ToDo: Implement
	def give_target(self):
		pass
		
	