from exceptions.exception import * # All the Exception Classes
from players.player import Player
from players.database import Database
from battleship.fleet import Fleet
from battleship.ships import *

import random

class AI(Player):

	def __init__(self):
		super().__init__()
		# triedPoints - a list of tuples representing the points already tried
		self.triedPoints = []
		# boardFrequency - a Dictionary of form Str:Lst[int] that stores the coordinate associated with the frequency of each ship being placed at that coordinate. Each of these numbers
		self.boardFrequency = []
		# self.likely_points = [False]
		# self.next_target = []
		self.successful_hits = []
		self.enemy_ships = 5
		self.direction=1
		self.found_point = False
		self.db = {}
		db = Database.get_instance().get_all()
		for row in list(db):
			spliced = row[1:]
			value = sum(spliced)/5 # Take the Average of the Values to Create the Likely Weight
			'''
			(COORDINATE, LIST, VALUE, LIKELY_SHIP_TYPE)
			'''
			self.boardFrequency.append((eval(row[0]),spliced,value,spliced.index(max(spliced))))
			self.db.update({eval(row[0]):(spliced,value,spliced.index(max(spliced)))})
		self.boardFrequency.sort(key = lambda i : i[2])

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
		testedAdjacent = 0

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
					self.successful_hits = [self.successful_hits[0]]
					self.direction+=1
					self.found_point = False
				else:
					self.successful_hits.append(self.triedPoints[-1])
					self.found_point = True
				target = self.sink_ship()

		else:
			if not opp.get_knowledge() and len(self.successful_hits) >= 2: # If reaches end of ship and miss
				print("ADVANCED: Turning Around")
				self.successful_hits = [self.successful_hits[0]]
				self.direction += 1 # Reverse Our Direction By Incrementing a Total of Two Times
				self.found_point = False
				target = self.sink_ship()
				if target in self.triedPoints:
					target = self.get_optimal()

			elif self.found_point: # If miss while trying a point to find direction
				print("ADVANCED: Trying Other Adjacent Points")
				target = self.sink_ship()
			else: # If Miss
				self.successful_hits = []
				target = self.get_optimal()
				self.found_point = False

		print("ADVANCED: Target is: ", target)

		while target in self.triedPoints:
			if testedAdjacent >= 3:
				target = self.get_optimal()
				break
			target = self.sink_ship()
			print("ADVANCED: New Target is ", target)
			testedAdjacent += 1
		if any(v>9 for v in target) or any(v<0 for v in target):
			raise InvalidCoordinateException("BAD COORDINATE")
		self.triedPoints.append(target)
		return target

	def get_optimal(self):
		pass


	# def target_adjacent(self): # Find the nearby points in cardinal directions tp a succesful hit
	# 	self.boardFrequency += self.likely_points[1:] #If there were previously stored likely points, promote them in board frequency
	# 	previousPoint = self.successful_hits[-1]
	# 	nearPoints = {}
	# 	for shift in range(-1,2): #Iterate Over the Range of Adjacent Points and Add if Novel and Untried
	# 		if (previousPoint[0]+shift,previousPoint[1]) not in self.triedPoints and 0<=previousPoint[0]+shift<=9:
	# 			# Retaining the Tuple Format of (COORDINATE, LIST, VALUE, LIKELY_SHIP_TYPE)
	# 			nearPoints.update({(previousPoint[0]+shift,previousPoint[1]):self.db[(previousPoint[0]+shift,previousPoint[1])]})
	# 		if (previousPoint[0],previousPoint[1]+shift) not in self.triedPoints and 0<=previousPoint[1]+shift<=9:
	# 			nearPoints.update({(previousPoint[0],previousPoint[1]+shift):self.db[(previousPoint[0],previousPoint[1]+shift)]})
	# 	nearPoints = [False] + [(k,v) for k, v in sorted(nearPoints.items())]
	# 	# Lambda Function that can be Added to the 'sorted' Function in the Above Line for Smarter Targeting: key=lambda item: item[1][2]
	# 	print( "Nearby Points are ", [tup[0] for tup in nearPoints[1:]])
	# 	return(nearPoints)
	#
	# def driver(self): # If the top two points of the stack are in the same row or column, find the points in that grouping.
	# 	self.likely_points = [] # Previous Adjacent Points are now Irrelevant, Since It's Been Narrowed to a Row/Col
	# 	first = self.successful_hits.pop()
	# 	second = self.successful_hits.pop()
	# 	row = []
	# 	for shift in range(-2,3):
	# 		x_values = [first[0]+shift,second[0]+shift]
	# 		y_values = [first[1]+shift,second[1]+shift]
	#
	# 		# Find Points Within +2 and -2 of the two points. This should result in a span of 6 units, which is enough to clear the carrier
	# 		if (first[0] == second[0]) and not any(y<0 for y in y_values) and not any(y>9 for y in y_values):
	# 			# Retaining the Tuple Format of (COORDINATE, LIST, VALUE, LIKELY_SHIP_TYPE)
	# 			row.append(((first[0],y_values[0]),self.db[(first[0],y_values[0])]))
	# 			row.append(((second[0],y_values[1]),self.db[(second[0],y_values[1])]))
	# 		elif (first[1] == second[1]) and not any(x<0 for x in x_values) and not any(x>9 for x in x_values):
	# 			row.append(((x_values[0],first[1]),self.db[(x_values[0],first[1])]))
	# 			row.append(((x_values[1],second[1]),self.db[(x_values[1],second[1])]))
	# 	if len(row) == 0:
	# 		# If there are no untested points in
	# 		self.successful_hits = self.successful_hits + [second,first]
	# 	ordered_row = [True] + [tup for tup in sorted(row) if tup[0] not in self.triedPoints] # Order Adjacent Points by Value
	# 	# ,key = lambda t : t[1][2]
	# 	print( "Ship's Row/Col is ", [tup[0] for tup in ordered_row[1:]])
	# 	return(ordered_row)

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
