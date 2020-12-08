from players.AI import AI

class Advanced(AI):

	def __init__(self):
		super().__init__()

	def get_optimal(self):
		optimal = self.boardFrequency.pop(-1)[0]
		while optimal in self.triedPoints and len(self.boardFrequency)>0:
			optimal = self.boardFrequency.pop(-1)[0]
		return optimal
