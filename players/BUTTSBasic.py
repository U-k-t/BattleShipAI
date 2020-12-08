from players.AI import AI

import random

class Basic(AI):

	def __init__(self):
		super().__init__()
		self.name = 'Basic'

	def get_optimal(self):
		optimal = (random.randint(0, 9), random.randint(0,9))
		while optimal in self.triedPoints:
			optimal = (random.randint(0, 9), random.randint(0,9))
		return(optimal)
