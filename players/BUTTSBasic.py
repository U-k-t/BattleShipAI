from players.AI import AI

import random

class Basic(AI):

	def __init__(self):
		super().__init__()

	# THIS IS RANDOM TARGET FOR TESTING
	# ToDo: Implement
	def give_target(self,opp):
		if opp.get_knowledge() and self.enemy_ships == len(opp.get_fleet()): # If opponent indicated last fire was a hit and no ships have sunk
			self.successful_hits.append(self.triedPoints[-1]) # Record the last succesful hit
			if len(self.successful_hits)>=2: # See if there are two hits in a row that we can follow the row of
				super().driver()
			else: # Otherwise, get the adjacent squares
				super().target_adjacent()
		elif self.enemy_ships > len(opp.get_fleet()): # "You sunk a ship!"
			self.enemy_ships-=1
			self.likely_points = [] # If we sunk a ship, our likely points default back to whatever we added to boardFrequency


		if len(self.likely_points) >0:
			self.next_target = self.likely_points
			optimal = self.next_target.pop(-1)[0] # Get the last item of the frequency list (has the highest odds of a ship being present)
			while optimal in self.triedPoints:
				optimal = self.next_target.pop(-1)[0]
		else:
			optimal = (random.randint(0, 9), random.randint(0,9))
			while optimal in self.triedPoints:
				optimal = (random.randint(0, 9), random.randint(0,9))
			self.triedPoints.append(optimal)
		return optimal
