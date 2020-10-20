import PySimpleGUI as sg # sg : simple gui
from repository.image_repository import ImageRepository # Repository of images as base 64
from exceptions.exception import * # All the Exception Classes
from battleship.ships import * # All the ship classes
from players.player import Player 
from players.AI import AI



'''***********************************************
	class Game:
		-Singleton Design: Only one instance allowed
***********************************************'''

class Game:
	
	__instance = None # Instance of class. 
	SHIP_NAMES = ["patrol", "submarine", "destroyer", "battleship", "carrier"]
	
	def __init__(self): #Throws an exception
		print("Create Game Object")
		
		if Game.__instance == None: # Does not exist
			Game.__instance = self
		else:
			raise Exception("Can not create multiple instances of class: Game")
		
		'''**************************
			Game Variables
		**************************'''
		self.player = Player()
		self.enemy = AI()
		self.turn = "position"
		
		self.window =  None
	
	@staticmethod
	def get_instance():
		if Game.__instance == None:
			Game()
		return Game.__instance
		
	@staticmethod				   
	def new_game(self):
		if Game.__instance == None:
			Game()
		else:
			self.player = Player()
			self.enemy = AI()
			self.turn = "position"
			
			if self.window != None:
				self.window.close()
			
		self.window = sg.Window("Battleship", self.create_ship_placement_layout(), icon = "assets/battleship.ico", margins = (30, 30))
		self.enemy.create_board()
	
	@staticmethod
	def end_game(self):
		if Game.__instance == None: 
			self.window.close()			
		
	def game_over(self, who_won):
		self.window.close()
		self.window = sg.Window("Battleship", self.create_game_over_layout(who_won), icon = "assets/battleship.ico", margins = (30, 30), finalize=True)
	
	def read(self):
		return self.window.read()
	
	def get_turn(self):
		return self.turn
	
	def next_turn(self):
		if self.turn == "position":
			if self.player.finish_board_placement():
				self.turn = "play"
			else: 
				raise BoardNotCompleteException("Player has not finished placing all ships")
	
	'''*******************************************
		Layout Methods
	*******************************************'''
	def toggle_ship_placement_buttons(self, value):
		for button_label in Game.SHIP_NAMES:
			self.window.FindElement(button_label).Update(disabled=value)
	
	def toggle_player_board_buttons(self, value):
		for row in range(Player.BOARD_SIZE):
			for col in range(Player.BOARD_SIZE):
				self.window.FindElement("Player " + str((row,col))).Update(disabled=value)
	
	def update_ui(self):
		if self.turn == "position":
			self.window.close()
			self.window = sg.Window("Battleship", self.create_ship_placement_layout(), icon = "assets/battleship.ico", margins = (30, 30))
		elif self.turn == "play":
			self.window.close()
			self.window = sg.Window("Battleship", self.create_game_layout(), icon = "assets/battleship.ico", margins = (30, 30), finalize=True)
			self.toggle_player_board_buttons(True)
			
	def __create_grid(self, board, type_of_button):
		board_layout = [[sg.Button('', image_data=board[row][col], button_color=(sg.theme_background_color(), sg.theme_background_color()), size = (4,2), pad=(0,0), key=type_of_button + str((row,col))) for col in range(Player.BOARD_SIZE)] for row in range(Player.BOARD_SIZE)]
		return board_layout
	
	def create_ship_placement_layout(self): # INITIAL Layout at begin of game. 
		# Menu Bar at the top. We can add other options for how we want to see stuff.
		menu_bar = [ ["Game", ["New Game", "Exit Game"]],
						  ["Help", ["How To Play"]]]

		# Start what the window will look like:
		layout = [[sg.Menu(menu_bar, tearoff = False, key="-MENU-")],
				  [sg.Text("Board Placements")],
				  [sg.Image('assets/battleship_title.png', size=(600,200))],
				  [sg.Text("Place each ship on the board by clicking the respected button")]]
		
		player_board_layout = [[sg.Text("Player Board:")]]
		player_board_layout += self.__create_grid(self.player.get_board(), "Player ") # Initializes each button with key "Player (row,col)"
	
		ship_button_layout = [[sg.Button('', image_data=ImageRepository.get_patrol_image(), button_color=(sg.theme_background_color(),sg.theme_background_color()), pad=(0,0), key="patrol")],
					  [sg.Button('', image_data=ImageRepository.get_submarine_image(), button_color=(sg.theme_background_color(),sg.theme_background_color()), pad=(0,0), key="submarine")],
					  [sg.Button('', image_data=ImageRepository.get_destroyer_image(), button_color=(sg.theme_background_color(),sg.theme_background_color()), pad=(0,0), key="destroyer")],
					  [sg.Button('', image_data=ImageRepository.get_battleship_image(), button_color=(sg.theme_background_color(),sg.theme_background_color()), pad=(0,0), key="battleship")],
					  [sg.Button('', image_data=ImageRepository.get_carrier_image(), button_color=(sg.theme_background_color(),sg.theme_background_color()), pad=(0,0), key="carrier")]]
					  
		
		layout += [[sg.Column(ship_button_layout),
				    sg.Column(player_board_layout)]]
						 
		layout += [[sg.Button("Confirm Placement", key="confirm"), sg.Button("Restart Placement", key="restart")]]

		return layout
	
	def create_game_layout(self):
		# Menu Bar at the top. We can add other options for how we want to see stuff.
		menu_bar = [ ["Game", ["New Game", "Exit Game"]],
						  ["Help", ["How To Play"]]]
	
		# Start what the window will look like:
		layout = [[sg.Menu(menu_bar, tearoff = False, key="-MENU-")],
				  [sg.Text("Player vs. BUTTS the Battleship game AI")],
				  [sg.Image('assets/battleship_title.png', size=(800,200))]]
				  
		player_board_layout = [[sg.Text("Player Board:")]]
		player_board_layout += self.__create_grid(self.player.get_board(), "Player ") # Initializes each button with key "Player (row,col)"
		
		enemy_board_layout = [[sg.Text("Enemy Board:")]]
		enemy_board_layout += self.__create_grid(self.enemy.get_board(), "Enemy ") # Initializes each button with key "Enemy (row,col)"
		
		ship_button_layout = [[sg.Image('assets/patrol.png')],
					  [sg.Image('assets/sub.png')],
					  [sg.Image('assets/destroyer.png')],
					  [sg.Image('assets/battleship.png')],
					  [sg.Image('assets/carrier.png')]]
		
		layout += [[sg.Column(ship_button_layout),
				    sg.Column(player_board_layout),
					sg.VSeperator(), # Line that separates the two.
					sg.Column(enemy_board_layout)]]
		
		return layout
	
	def create_game_over_layout(self, who_won):
		# Menu Bar at the top. We can add other options for how we want to see stuff.
		menu_bar = [ ["Game", ["New Game", "Exit Game"]],
					 ["Help", ["How To Play"]]]
					 
		# Start what the window will look like:
		layout = [[sg.Menu(menu_bar, tearoff = False, key="-MENU-")],
				  [sg.Text("Player vs. BUTTS the Battleship game AI")],
				  [sg.Image('assets/battleship_title.png', size=(400,200))]]
				  
		layout += [[sg.Text("GAME OVER!" + who_won )],
				   [sg.Text("Play again?")],
				   [sg.Button("Yes", key="New Game"), sg.Button("No", key="Exit Game")]]
	   
		return layout
	
	'''*******************************************
		Ship Placement Set Up Methods
	*******************************************'''
	def on_click_patrol_button(self, start, end):
		self.player.place_ship(Patrol(start,end), False)
		
	def on_click_submarine_button(self, start, end):
		self.player.place_ship(Submarine(start, end), False)
		
	def on_click_destroyer_button(self, start, end):
		self.player.place_ship(Destroyer(start, end), False)
		
	def on_click_battleship_button(self, start, end):
		self.player.place_ship(Battleship(start, end), False)
		
	def on_click_carrier_button(self, start, end):
		self.player.place_ship(Carrier(start, end), False)
		
	'''*******************************************
		In Game Action Methods
	*******************************************'''
	def attack_enemy(self, target):
		try:
			if self.enemy.defend(target):
				# GAME OVER, player win!
				print("Player won!")
				self.game_over("player won!")
				return False
			return True # sucessful attack
		except(AlreadyPointTakenException):
			print("Invalid target given by Player")
			return False
	
	def attack_player(self):
		try: 
			if self.player.defend(self.enemy.give_target()):
				# GAME OVER, AI win!
				self.game_over("AI won!")
				return False
			return True # sucessful attack 
		except(AlreadyPointTakenException):
			print("Invalid target given by AI")
			return False
	
def main():
	
	Game.new_game(Game())
	game = Game.get_instance()
	
	# TODO: Add Turn based event check
	#  [] Ship Placement Turn (AI Does in background)
	#  [x] Player Goes first, Turn based
	#  [] Refreshes board layout after turn taken
	# Reminders: MUST CATCH EXCEPTIONS
	
	wait = 0 # Forces the player to perform 2 actions. There is a better way to do this, but idk how yet. 
	startcoord = -1
	endcoord = -1
	
	#Event Loop:
	while True:
		event, values = game.read()
		
		# event = the string that represents the key of a button pressed.
		if event == sg.WIN_CLOSED or event == "Exit Game":
			# If user chooses to exit the game
			Game.end_game(game)
			break
		elif event == "New Game":
			print("New Game Pressed")
			Game.new_game(game)
		elif event == "How To Play":
			# Instructions on how to play (we can remove this)
			print("Help Pressed")
		elif event == "confirm" and wait == 0:
			# Placed Ships
			try:
				game.next_turn() # TODO: raises an exception MUST be caught
				game.update_ui()
				wait = 1
			except (BoardNotCompleteException):
				print("Missing number of ship requirements")
		elif event == "restart":
			wait = 0
			Game.new_game(game)
		else:
			if game.get_turn() == "position": # If turn is for placing ships. 
				
				if wait == 2 and "Player" in event:
					startcoord = eval(event.replace("Player ", ""))
					wait -= 1
				elif wait == 1 and "Player" in event:
					endcoord = eval(event.replace("Player ", ""))
					wait = 0
					
					try: 
						eval(clicked + str(startcoord) + "," + str(endcoord) + ")")
						game.toggle_ship_placement_buttons(False)

					except InvalidShipException as ex:
						print("exception thrown, continue program: " + str(ex)) # Temporary action. 
					
					game.update_ui()
					
				elif event in Game.SHIP_NAMES:
					game.toggle_ship_placement_buttons(True)
					wait = 2
					clicked = "game.on_click_" + event + "_button("
			else: # If its player or AI turn. 
				if wait == 1 and "Enemy" in event:
					attack_coords = eval(event.replace("Enemy ", ""))
					if game.attack_enemy(attack_coords):
						# PERFORM AI TURN HERE
						game.attack_player()
						game.update_ui()
						
					


main()
