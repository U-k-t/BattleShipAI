from players.AI import AI
from players.database import Database

class Advanced(AI):

	def __init__(self):
		super().__init__()
		# boardFrequency - a Dictionary of form Str:Lst[int] that stores the coordinate associated with the frequency of each ship being placed at that coordinate. Each of these numbers
		self.boardFrequency = []
		self.db = {}
		db = Database.get_instance().get_all()
		games = Database.get_instance().get_games_played()
		for row in list(db):
			spliced = [x/games for x in row[1:]]
			value = sum(spliced)/5 # Take the Average of the Values to Create the Likely Weight
			'''
			(COORDINATE, LIST, VALUE, LIKELY_SHIP_TYPE)
			'''
			self.boardFrequency.append((eval(row[0]),spliced,value,spliced.index(max(spliced))))
			self.db.update({eval(row[0]):(spliced,value,spliced.index(max(spliced)))})
		self.boardFrequency.sort(key = lambda i : i[2])


	def get_optimal(self):
		optimal = self.boardFrequency.pop(-1)[0]
		while optimal in self.triedPoints and len(self.boardFrequency)>0:
			optimal = self.boardFrequency.pop(-1)[0]
		return optimal
