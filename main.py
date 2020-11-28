import PySimpleGUI as sg # sg : simple gui
from repository.image_repository import ImageRepository # Repository of images as base 64
from exceptions.exception import * # All the Exception Classes
from players.database import Database
from battleship.ships import * # All the ship classes
from players.player import Player 
from players.AI import AI
from players.BUTTSBasic import Basic
from players.BUTTS import Advanced

import time


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
		self.player1 = None
		self.player2 = None
		self.turn = None
		
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
			if self.window != None:
				self.window.close()
			
		self.window = sg.Window("Battleship", self.create_init_menu_layout(), icon = "assets/battleship.ico", margins = (30, 30))
	
	@staticmethod
	def new_player_vs_basic(self):
		print( "Selected game mode: Player vs Basic AI")
		self.player1 = Player()
		self.player2 = Basic()
		self.turn = "position"
		
		self.window.close()
		self.window = sg.Window("Battleship", self.create_ship_placement_layout(), icon = "assets/battleship.ico", margins = (30, 30))
		self.player2.create_board()
		
	@staticmethod
	def new_player_vs_advanced(self):
		print( "Selected game mode: Player vs Advanced AI")
		self.player1 = Player()
		self.player2 = Advanced()
		self.turn = "position"
		
		self.window.close()
		self.window = sg.Window("Battleship", self.create_ship_placement_layout(), icon = "assets/battleship.ico", margins = (30, 30))
		self.player2.create_board()
	
	@staticmethod
	def new_basic_vs_advanced(self):
		print( "Selected game mode: Basic AI vs Advanced AI")
		self.player1 = Basic()
		self.player2 = Advanced()
		self.turn = "battle"
		
		self.player1.create_board()
		self.player2.create_board()
		self.window.close()
		self.window = sg.Window("Battleship", self.create_ai_battle_layout(), icon = "assets/battleship.ico", margins = (30, 30))

	
	
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
			if self.player1.finish_board_placement():
				Database.get_instance().save_board(self.player1.get_fleet())
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
			self.toggle_player_board_buttons(true)
		elif self.turn == "battle":
			self.window.close()
			self.window = sg.Window("Battleship", self.create_ai_battle_layout(), icon = "assets/battleship.ico", margins = (30, 30), finalize=True)
			
	def __create_grid(self, board, type_of_button):
		board_layout = [[sg.Button('', image_data=board[row][col], button_color=(sg.theme_background_color(), sg.theme_background_color()), size = (4,2), pad=(0,0), key=type_of_button + str((row,col))) for col in range(Player.BOARD_SIZE)] for row in range(Player.BOARD_SIZE)]
		return board_layout
	
	def create_init_menu_layout(self): # INITIAL Layout at begin of game. 
		# Menu Bar at the top. We can add other options for how we want to see stuff.
		menu_bar = [ ["Game", ["New Game", "Exit Game"]],
						  ["Help", ["How To Play"]]]
						  
		# Start what the window will look like:
		layout = [[sg.Menu(menu_bar, tearoff = False, key="-MENU-")],
				  [sg.Text("Main Menu")],
				  [sg.Image('assets/battleship_title.png', size=(600,200))]]
		
		button_selection_layout = [[sg.Button('You vs Basic AI', key="basic")],
								   [sg.Button('You vs Advanced AI', key="advanced")],
								   [sg.Button('Watch the AI\'s battle it out', key="battle")]]
		layout += button_selection_layout
		return layout
				  
				  
	def create_ship_placement_layout(self): 
		# Menu Bar at the top. We can add other options for how we want to see stuff.
		menu_bar = [ ["Game", ["New Game", "Exit Game"]],
						  ["Help", ["How To Play"]]]

		# Start what the window will look like:
		layout = [[sg.Menu(menu_bar, tearoff = False, key="-MENU-")],
				  [sg.Text("Board Placements")],
				  [sg.Image('assets/battleship_title.png', size=(600,200))],
				  [sg.Text("Place each ship on the board by clicking the respected button")]]
		
		player_board_layout = [[sg.Text("Player Board:")]]
		player_board_layout += self.__create_grid(self.player1.get_board(), "Player ") # Initializes each button with key "Player (row,col)"
	
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
		player_board_layout += self.__create_grid(self.player1.get_board(), "Player ") # Initializes each button with key "Player (row,col)"
		
		enemy_board_layout = [[sg.Text("Enemy Board:")]]
		enemy_board_layout += self.__create_grid(self.player2.get_board(), "Enemy ") # Initializes each button with key "Enemy (row,col)"
				
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
	
	def create_ai_battle_layout(self):
		# Menu Bar at the top. We can add other options for how we want to see stuff.
		menu_bar = [ ["Game", ["New Game", "Exit Game"]],
						  ["Help", ["How To Play"]]]
	
		# Start what the window will look like:
		layout = [[sg.Menu(menu_bar, tearoff = False, key="-MENU-")],
				  [sg.Text("Battle of the BUTTS: Basic vs Advanced")],
				  [sg.Image('assets/battleship_title.png', size=(600,200))]]
				
		player_board_layout = [[sg.Text("Basic Board:")]]
		player_board_layout += self.__create_grid(self.player1.get_board(), "Player ") # Initializes each button with key "Player (row,col)"
		
		enemy_board_layout = [[sg.Text("Advanced Board:")]]
		enemy_board_layout += self.__create_grid(self.player2.get_board(), "Enemy ") # Initializes each button with key "Enemy (row,col)"
				
		
		layout += [[sg.Column(player_board_layout),
					sg.VSeperator(), # Line that separates the two.
					sg.Column(enemy_board_layout)],
					[sg.Button("Next", key="next")]]
		
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
		self.player1.place_ship(Patrol(start,end), False)
		
	def on_click_submarine_button(self, start, end):
		self.player1.place_ship(Submarine(start, end), False)
		
	def on_click_destroyer_button(self, start, end):
		self.player1.place_ship(Destroyer(start, end), False)
		
	def on_click_battleship_button(self, start, end):
		self.player1.place_ship(Battleship(start, end), False)
		
	def on_click_carrier_button(self, start, end):
		self.player1.place_ship(Carrier(start, end), False)
		
	'''*******************************************
		In Game Action Methods
	*******************************************'''
	def attack_enemy(self, target):
		try:
			if self.player2.defend(target):
				# GAME OVER, player win!
				print("Player won!")
				self.game_over("player won!")
				return False
			return True # sucessful attack
		except(AlreadyPointTakenException):
			print("Invalid target given by Player")
			return False
	
	def attack_player1(self):
		try: 
			if self.player1.defend(self.player2.give_target()):
				# GAME OVER, Advanced win!
				self.game_over("Advanced won!")
				return False
			return True # sucessful attack 
		except(AlreadyPointTakenException):
			print("Invalid target given by AI: Advanced")
			return False
			
	def attack_player2(self):
		try: 
			if self.player2.defend(self.player1.give_target()):
				# GAME OVER, Basic win!
				self.game_over("Basic won!")
				return False
			return True # sucessful attack 
		except(AlreadyPointTakenException):
			print("Invalid target given by AI: Basic")
			return False
			
	
# Reminders: MUST CATCH EXCEPTIONS
def main():
	
	Game.new_game(Game())
	game = Game.get_instance()
	
	wait = 0 # Forces the player to perform 2 actions. There is a better way to do this, but idk how yet. 
	startcoord = -1
	endcoord = -1
	next = 1
	
	#Event Loop:
	while True:
		event, values = Game.get_instance().read()
		
		# event = the string that represents the key of a button pressed.
		if event == sg.WIN_CLOSED or event == "Exit Game":
			# If user chooses to exit the game
			Game.end_game(Game.get_instance())
			break
		elif event == "New Game":
			print("New Game Pressed")
			Game.new_game(Game.get_instance())
		elif event == "basic":
			Game.new_player_vs_basic(Game.get_instance())
		elif event == "advanced":
			Game.new_player_vs_advanced(Game.get_instance())
		elif event == "battle":
			Game.new_basic_vs_advanced(Game.get_instance())
		elif event == "How To Play":
			# Instructions on how to play (we can remove this)
			print("Help Pressed")
		elif event == "next": # Not a player vs Ai game but an AI vs AI game. (rest of the checks pointless)
			if next % 2 == 0:
				Game.get_instance().attack_player1()
				Game.get_instance().update_ui()
			else:
				Game.get_instance().attack_player2()
				Game.get_instance().update_ui()
			
			next = next + 1
			

		elif event == "confirm" and wait == 0:
			# Placed Ships
			try:
				Game.get_instance().next_turn() 
				Game.get_instance().update_ui()
				wait = 1
			except (BoardNotCompleteException):
				print("Missing number of ship requirements")
		elif event == "restart":
			wait = 0
			Game.new_game(Game.get_instance())
		else:
			if Game.get_instance().get_turn() == "position": # If turn is for placing ships. 
				
				if wait == 2 and "Player" in event:
					startcoord = eval(event.replace("Player ", ""))
					wait -= 1
				elif wait == 1 and "Player" in event:
					endcoord = eval(event.replace("Player ", ""))
					wait = 0
					
					try: 
						eval(clicked + str(startcoord) + "," + str(endcoord) + ")")
						Game.get_instance().toggle_ship_placement_buttons(False)

					except InvalidShipException as ex:
						print("exception thrown, continue program: " + str(ex)) # Temporary action. 
					
					Game.get_instance().update_ui()
					
				elif event in Game.SHIP_NAMES:
					Game.get_instance().toggle_ship_placement_buttons(True)
					wait = 2
					clicked = "Game.get_instance().on_click_" + event + "_button("
			elif Game.get_instance().get_turn() == "play": # If its player or AI turn in a player vs AI game 
				if wait == 1 and "Enemy" in event:
					attack_coords = eval(event.replace("Enemy ", ""))
					if Game.get_instance().attack_enemy(attack_coords):
						# PERFORM AI TURN HERE
						Game.get_instance().attack_player1()
						Game.get_instance().update_ui()


main()
