from players.AI import AI

class Advanced(AI):

	def __init__(self):
		super().__init__()
		
	def give_target(self, opp): # Targets based off of knowledge from the database 
		if opp.get_knowledge() and self.enemy_ships == len(opp.get_fleet()): # If opponent indicated last fire was a hit and no ships have sunk
			self.successful_hits.append(eval(self.triedPoints[-1])) # Record the last succesful hit
			if len(self.successful_hits)>=2: # See if there are two hits in a row that we can follow the row of
				self.boardFrequency = self.boardFrequency + super.driver()
			else: # Otherwise, get the adjacent squares
				self.boardFrequency = self.boardFrequency + super.target_adjacent()
		elif self.enemy_ships > len(opp.get_fleet()): # "You sunk a ship!"
			self.enemy_ships-=1
		optimal = self.boardFrequency.pop(-1) # Get the last item of the frequency list (has the highest odds of a ship being present)
		while optimal[0] in self.triedPoints:
			optimal = self.boardFrequency.pop(-1)
		self.triedPoints.append(optimal[0])
		return eval(optimal[0])
