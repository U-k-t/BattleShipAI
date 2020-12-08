from players.AI import AI

class Advanced(AI):

	def __init__(self):
		super().__init__()

	# def give_target(self, opp): # Targets based off of knowledge from the database
	#
	# 	if opp.get_knowledge() and self.enemy_ships == len(opp.get_fleet()): # If opponent indicated last fire was a hit and no ships have sunk
	# 		self.successful_hits.append(self.triedPoints[-1]) # Record the last succesful hit
	# 		print("Last hit was succesful")
	# 		if len(self.successful_hits)>=2: # See if there are two hits in a row that we can follow the row of
	# 			self.likely_points =  super().driver()
	# 		elif not self.likely_points[0]: # Otherwise, get the adjacent squares
	# 			print ("Advanced AI: Identifying Adjacent Points")
	# 			self.likely_points =  super().target_adjacent()
	# 	elif self.enemy_ships > len(opp.get_fleet()): # "You sunk a ship!"
	# 		self.enemy_ships-=1
	# 		self.likely_points = [False] # If we sunk a ship, our likely points default back to whatever we added to boardFrequency
	#
	#
	# 	if len(self.likely_points) >1:
	# 		print("Advanced AI: Targeting Likely Points")
	# 		self.next_target = self.boardFrequency+self.likely_points[1:]
	# 	else:
	# 		print("Advanced AI: Using Database Knowledge")
	# 		self.next_target = self.boardFrequency
	# 	optimal = self.next_target.pop(-1) # Get the last item of the frequency list (has the highest odds of a ship being present)
	# 	while optimal[0] in self.triedPoints and len(self.next_target)>0:
	# 		optimal = self.next_target.pop(-1)
	# 	self.triedPoints.append(optimal[0])
	# 	print("Advanced AI:  Next Target is ", optimal[0])
	# 	return optimal[0]

	def get_optimal(self):
		optimal = self.boardFrequency.pop(-1)[0]
		while optimal in self.triedPoints and len(self.boardFrequency)>0:
			optimal = self.boardFrequency.pop(-1)[0]
		return optimal
