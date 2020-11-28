from players.AI import AI

import random

class Basic(AI):
	
	def __init__(self):
		super().__init__()
		
	# THIS IS RANDOM TARGET FOR TESTING 
	# ToDo: Implement
	def give_target(self):
		return (random.randint(0, 9), random.randint(0,9))