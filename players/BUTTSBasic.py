from players.AI import AI

import random

class Basic(AI):

	def __init__(self):
		super().__init__()

	# THIS IS RANDOM TARGET FOR TESTING
	# ToDo: Implement
	def give_target(self,opp):
		# if opp.get_knowledge() and self.enemy_ships == len(opp.get_fleet()):
		# 	self.successful_hits.append(self.triedPoints[-1]) # Record the last succesful hit
		# 	if len(self.successful_hits)>=2: # See if there are two hits in a row that we can follow the row of
		# 		self.boardFrequency = self.boardFrequency + super().driver()
		# else:
		# 	random_point = random.randint(0, 9), random.randint(0,9)
		# 	self.triedPoints.append(random_point)
		# 	return (random_point)
		return(random.randint(0, 9), random.randint(0,9))
