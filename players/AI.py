from exceptions.exception import * # All the Exception Classes
from players.player import Player
from players.database import Database
from battleship.fleet import Fleet
from battleship.ships import *
import numpy as np

import random

class AI(Player):

	def __init__(self):
		super().__init__()
		# triedPoints - a list of tuples representing the points already tried
		self.triedPoints = []
		# boardFrequency - a Dictionary of form Str:Lst[int] that stores the coordinate associated with the frequency of each ship being placed at that coordinate. Each of these numbers
		self.boardFrequency = []
		self.successful_hits = []
		self.enemy_ships = 5
		self.db = {}
		db = Database.get_instance().get_all()
		for row in list(db):
			spliced = row[1:]
			value = max(spliced)
			'''
			(COORDINATE, LIST, MAXIMUM, SHIP_TYPE)
			'''
			self.boardFrequency.append((row[0],np.array(spliced),value,spliced.index(value)))
			self.db.update({row[0]:(np.array(spliced),value,spliced.index(value))})
		self.boardFrequency.sort(key = lambda i : i[2])
		for item in self.boardFrequency:
			print(item)

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
		pass

	def target_adjacent(self): # Find the nearby points in cardinal directions tp a succesful hit
		previousPoint = self.successful_hits[-1]
		nearPoints = {}
		for shift in range(-1,2):
			if (previousPoint[0]+shift,previousPoint[1]) not in self.triedPoints and 0>=previousPoint[0]+shift>=9:
				nearPoints.update({(previousPoint[0]+shift,previousPoint[1]):self.db[str((previousPoint[0]+shift,previousPoint[1]))]})
			if (previousPoint[0],previousPoint[1]+shift) not in self.triedPoints and 0>=previousPoint[1]+shift>=9:
				nearPoints.update({(previousPoint[0],previousPoint[1]+shift):self.db[str((previousPoint[0],previousPoint[1]+shift))]})
		nearPoints = [(str(k),v) for k, v in sorted(nearPoints.items(), key=lambda item: item[1][2])] # Order the adjacent points by their value
		return nearPoints

	def driver(self): # If the top two points of the stack are in the same row or column, find the points in that grouping.
		first = self.successful_hits.pop()
		second = self.successful_hits.pop()
		row = []
		for shift in range(-2,3):
			x_values = [first[0]+shift,second[0]+shift]
			y_values = [first[1]+shift,second[1]+shift]
			if (first[0] == second[0]) and not any(y<0 for y in y_values) and not any(y>9 for y in y_values):
				row.append((str((first[0],y_values[0])),self.db[str((first[0],y_values[0]))]))
				row.append((str((second[0],y_values[1])),self.db[str((second[0],y_values[1]))]))
			elif (first[1] == second[1]) and not any(x<0 for x in x_values) and not any(x>9 for x in x_values):
				row.append((str((x_values[0],first[1])),self.db[str((x_values[0],first[1]))]))
				row.append((str((x_values[1],second[1])),self.db[str((x_values[1],second[1]))]))
		if len(row) == 0:
			self.successful_hits = self.successful_hits + [second,first]
		ordered_row = [tup for tup in sorted(row,key = lambda t : t[1][2]) if tup[0] not in self.triedPoints] # Order Adjacent Points by Value
		return ordered_row
