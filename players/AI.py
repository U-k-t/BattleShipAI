from exceptions.exception import * # All the Exception Classes
from players.player import Player
from players.database import Database
from battleship.fleet import Fleet
from battleship.ships import *
import numpy as np

import random

'''TODO: Implement '''



 # We can inherit from this to make a Butts / Butts Basic potentially
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
		db = Database.get_instance().connection.execute("SELECT * from Storage;")
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

	def smart_target(self,opp):
		if opp.get_knowledge() and self.enemy_ships == len(opp.get_fleet()): # If opponent indicated last fire was a hit and no ships have sunk
			self.successful_hits.append(eval(self.triedPoints[-1])) # Record the last succesful hit
			if len(self.successful_hits)>=2: # See if there are two hits in a row that we can follow the row of
				self.boardFrequency = self.boardFrequency + self.driver()
			else: # Otherwise, get the adjacent squares
				self.boardFrequency = self.boardFrequency + self.target_adjacent()
		elif self.enemy_ships > len(opp.get_fleet()): # "You sunk a ship!"
			self.enemy_ships-=1
		optimal = self.boardFrequency.pop(-1) # Get the last item of the frequency list (has the highest odds of a ship being present)
		while optimal[0] in self.triedPoints:
			optimal = self.boardFrequency.pop(-1)
		self.triedPoints.append(optimal[0])
		return eval(optimal[0])

	def target_adjacent(self): # Find the nearby points in cardinal directions tp a succesful hit
		previousPoint = self.successful_hits[-1]
		nearPoints = {}
		for shift in range(-1,2):
			if (previousPoint[0]+shift,previousPoint[1]) not in self.triedPoints:
				nearPoints.update({(previousPoint[0]+shift,previousPoint[1]):self.db[str((previousPoint[0]+shift,previousPoint[1]))]})
			if (previousPoint[0],previousPoint[1]+shift) not in self.triedPoints:
				nearPoints.update({(previousPoint[0],previousPoint[1]+shift):self.db[str((previousPoint[0],previousPoint[1]+shift))]})
		nearPoints = [(str(k),v) for k, v in sorted(nearPoints.items(), key=lambda item: item[1][2])] # Order the adjacent points by their value
		return nearPoints

	def driver(self): # If the top two points of the stack are in the same row or column, find the points in that grouping.
		first = self.successful_hits.pop()
		second = self.successful_hits.pop()
		row = []
		for shift in range(-2,3):
			if (first[0] == second[0]):
				row.append((str((first[0],first[1]+shift)),self.db[str((first[0],first[1]+shift))]))
				row.append((str((second[0],second[1]+shift)),self.db[str((second[0],second[1]+shift))]))
			elif (first[1] == second[1]):
				row.append((str((first[0]+shift,first[1])),self.db[str((first[0]+shift,first[1]))]))
				row.append((str((second[0]+shift,second[1])),self.db[str((second[0]+shift,second[1]))]))
		if len(row) == 0:
			self.successful_hits = self.successful_hits + [second,first]
		ordered_row = [tup for tup in sorted(row,key = lambda t : t[1][2]) if tup[0] not in self.triedPoints] # Order Adjacent Points by Value
		return ordered_row
