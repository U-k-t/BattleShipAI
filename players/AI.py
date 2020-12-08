from exceptions.exception import * # All the Exception Classes
from players.player import Player
from battleship.fleet import Fleet
from battleship.ships import *

import random

class AI(Player):

	def __init__(self):
		super().__init__()
		# triedPoints - a list of tuples representing the points already tried
		self.triedPoints = []
		self.successful_hits = []
		self.enemy_ships = 5
		self.direction=1
		self.found_point = False
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


	def give_target(self, opp):

		if opp.get_knowledge():
			if self.enemy_ships > len(opp.get_fleet()): # If Hit and Sunk
				print("ADVANCED: Sunk an Enemy Ship")
				self.enemy_ships -= 1
				self.found_point = False
				self.successful_hits = []
				target = self.get_optimal()
			else: # If Hit and Didn't Sink
				print("ADVANCED: Hit, Did Not Sink")
				if self.triedPoints[-1] in self.successful_hits:
					target = self.reverse_direction()
				else:
					self.successful_hits.append(self.triedPoints[-1])
					self.found_point = True
					target = self.sink_ship()

		else:
			if len(self.successful_hits) >= 2: # If reaches end of ship and miss
				target = self.reverse_direction()

			elif self.found_point: # If miss while trying a point to find direction
				print("ADVANCED: Trying Other Adjacent Points")
				target = self.sink_ship()
				previous = self.successful_hits[-1]
				surrounding = [(previous[0]+x, previous[1]) for x in range(-1,2) if 0<=previous[0]+x<=9] + [(previous[0], previous[1]+y) for y in range(-1,2) if 0<=previous[1]+y<=9]
				if(set(surrounding).issubset(set(self.triedPoints))):
					print("is_subset")
					target = self.reverse_direction()
			else: # If Miss
				self.successful_hits = []
				target = self.get_optimal()
				self.found_point = False

		print("ADVANCED: Target is: ", target)

		if any(v>9 for v in target) or any(v<0 for v in target):
			raise InvalidCoordinateException("BAD COORDINATE")

		self.triedPoints.append(target)
		return target

	def get_optimal(self):
		pass

	def sink_ship(self):
		print(self.successful_hits)
		if len(self.successful_hits) <2: #If the system isn't "Locked On"
			self.direction +=1
			if self.direction >= 5:
				self.direction = self.direction%4 # Flip the Direction
		next_attack = self.get_directions(self.successful_hits[-1],self.direction)

		return next_attack

	def get_directions(self,coords,direction):
		print("coords: ", coords, " direction, ", direction)
		directions = {
		1: (-1,0),
		2: (0,1),
		3: (1,0),
		4: (0,-1)
		}
		move = directions[direction]
		target = (coords[0]+move[0], coords[1]+move[1])
		return target
	def reverse_direction(self):
		print("ADVANCED: Turning Around")
		self.successful_hits = [self.successful_hits[0]]
		self.direction += 1 # Reverse Our Direction By Incrementing a Total of Two Times
		self.found_point = False
		target = self.sink_ship()
		if target in self.triedPoints:
			target = self.get_optimal()
		return target
