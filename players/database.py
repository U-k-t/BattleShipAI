import sqlite3

class Database:

	__instance = None #instance of class.

	def __init__(self):
		print("Create Database Object")

		if Database.__instance == None: # Does not exist
			Database.__instance = self
		else:
			raise Exception("Can not create multiple instances of class: Database")

		'''****************************
			Database variables
		****************************'''
		self._connection = sqlite3.connect('assets/battleship.db')
		#self.c = connection.cursor()

	@staticmethod
	def get_instance():
		if Database.__instance == None:
			Database()
		return Database.__instance

	def get_value(self, coord, ship_name):
		return int(self._connection.execute("SELECT {} FROM Storage WHERE coord = \"{}\"".format(ship_name, str(coord))).fetchone()[0])

	def update_game(self):
		self._connection.execute("UPDATE History SET game = game + 1")
		self._connection.commit()

	def get_games_played(self):
		return int(self._connection.execute("SELECT * FROM History").fetchone()[0])

	def update(self, coord, ship_name):
		value = self.get_value(coord, ship_name)
		value = value + 1
		self._connection.execute("UPDATE Storage SET {}={} WHERE coord = \"{}\";".format(ship_name, value, str(coord)))
		self._connection.commit()

	def save_board(self, enemy_fleet):
		for ship in enemy_fleet:
			for coord in ship.get_coord():
				self.update(coord, ship.get_name())


	def get_all(self):
		return self._connection.execute("SELECT * from Storage;")
