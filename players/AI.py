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

	def smart_target(self):
		if super().get_knowledge():
			print("Target Adjacent")
			pass
			# return target_adjacent()
		optimal = self.boardFrequency.pop(-1) # Get the last item of the frequency list (has the highest odds of a ship being present)
		print(optimal)
		if optimal[0] not in self.triedPoints:
			self.triedPoints.append(optimal[0])
			return eval(optimal[0])
		else:
			self.smart_target()

	def target_adjacent(self):
		previousPoint = self.triedPoints[-1]
		nearPoints = {}
		for shift in range(-1,2):
			if (previousPoint[0]+shift,previousPoint[1]) not in self.triedPoints:
				nearPoints.update({(previousPoint[0]+shift,previousPoint[1]):self.db[(previousPoint[0]+shift,previousPoint[1])]})
			if (previousPoint[0],previousPoint[1]+shift) not in self.triedPoints:
				nearPoints.update({(previousPoint[0],previousPoint[1]+shift):self.db[(previousPoint[0],previousPoint[1]+shift)]})
		nearPoints = [k for k, v in sorted(nearPoints.items(), key=lambda item: item[1])]
		return nearPoints




		pass
