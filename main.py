import PySimpleGUI as sg # sg : simple gui
from repository.image_repository import ImageRepository
from battleship.ships import *
from player import Player
from AI import AI

# thrown if board is not initialized with ships. 
class BoardNotCompleteException(Exception):
	pass

class Game:

	def __init__(self):
		print("Create Game Object")
		
		'''**************************
			Game Variables
		**************************'''
		self.player = Player()
		self.enemy = AI()
		self.turn = "position"
		

					   
				
	def get_turn(self):
		return self.turn
	
	def next_turn(self):
		if self.turn == "position":
			if self.player.finish_board_placement():
				self.turn = "player"
			else: 
				raise BoardNotCompleteException("Player has not finished placing all ships")
	
	
	def create_layout(self): # INITIAL Layout at begin of game. 
		
		'''
		# board layout: Player left column, enemy right column
		sg.VSeperator(), # Line that separates the two.
		enemy_board_layout = [[sg.Text("Enemy Board:")]]
		enemy_board_layout += self.__create_grid(self.enemy.get_board(), "Enemy ") # Initializes each button with key "Enemy (row,col)"
		'''
		# Menu Bar at the top. We can add other options for how we want to see stuff.
		menu_bar = [ ["Game", ["New Game", "Exit Game"]],
						  ["Help", ["How To Play"]]]

		# Start what the window will look like:
		layout = [[sg.Menu(menu_bar, tearoff = False, key="-MENU-")],
					   [sg.Text("Player vs. BUTTS the Battleship game AI")],
					   [sg.Image('assets/battleship_title.png', size=(600,200))]]
		
		player_board_layout = [[sg.Text("Player Board:")]]
		player_board_layout += self.__create_grid(self.player.get_board(), "Player ") # Initializes each button with key "Player (row,col)"
		
		ship_button_layout = [[sg.Button('', image_data=ImageRepository.get_patrol_image(), button_color=(sg.theme_background_color(),sg.theme_background_color()), pad=(0,0), key="patrol")],
							  [sg.Button('', image_data=ImageRepository.get_submarine_image(), button_color=(sg.theme_background_color(),sg.theme_background_color()), pad=(0,0), key="submarine")],
							  [sg.Button('', image_data=ImageRepository.get_destroyer_image(), button_color=(sg.theme_background_color(),sg.theme_background_color()), pad=(0,0), key="destroyer")],
							  [sg.Button('', image_data=ImageRepository.get_battleship_image(), button_color=(sg.theme_background_color(),sg.theme_background_color()), pad=(0,0), key="battleship")],
							  [sg.Button('', image_data=ImageRepository.get_carrier_image(), button_color=(sg.theme_background_color(),sg.theme_background_color()), pad=(0,0), key="carrier")]]
							  
		
		layout += [[sg.Column(ship_button_layout),
						 sg.Column(player_board_layout, key="player_board")]]
						 
		layout += [[sg.Button("Confirm Placement", key="confirm"), sg.Button("Restart Placement", key="restart")]]

		return layout

	def __create_grid(self, board, type_of_button):
		board_layout = [[sg.Button('', image_data=board[row][col], button_color=(sg.theme_background_color(), sg.theme_background_color()), size = (4,2), pad=(0,0), key=type_of_button + str((row,col))) for col in range(10)] for row in range(10)]
		return board_layout
	
	def update_ui(self):
		# Menu Bar at the top. We can add other options for how we want to see stuff.
		menu_bar = [ ["Game", ["New Game", "Exit Game"]],
						  ["Help", ["How To Play"]]]

		# Start what the window will look like:
		layout = [[sg.Menu(menu_bar, tearoff = False, key="-MENU-")],
					   [sg.Text("Player vs. BUTTS the Battleship game AI")],
					   [sg.Image('assets/battleship_title.png', size=(600,200))]]
		
	
		player_board_layout = [[sg.Text("Player Board:")]]
		player_board_layout += self.__create_grid(self.player.get_board(), "Player ") # Initializes each button with key "Player (row,col)"
		
		ship_button_layout = [[sg.Button('', image_data=ImageRepository.get_patrol_image(), button_color=(sg.theme_background_color(),sg.theme_background_color()), pad=(0,0), key="patrol")],
							  [sg.Button('', image_data=ImageRepository.get_submarine_image(), button_color=(sg.theme_background_color(),sg.theme_background_color()), pad=(0,0), key="submarine")],
							  [sg.Button('', image_data=ImageRepository.get_destroyer_image(), button_color=(sg.theme_background_color(),sg.theme_background_color()), pad=(0,0), key="destroyer")],
							  [sg.Button('', image_data=ImageRepository.get_battleship_image(), button_color=(sg.theme_background_color(),sg.theme_background_color()), pad=(0,0), key="battleship")],
							  [sg.Button('', image_data=ImageRepository.get_carrier_image(), button_color=(sg.theme_background_color(),sg.theme_background_color()), pad=(0,0), key="carrier")]]
							  
		
		layout += [[sg.Column(ship_button_layout),
						 sg.Column(player_board_layout, key="player_board")]]
						 
		layout += [[sg.Button("Confirm Placement", key="confirm"), sg.Button("Restart Placement", key="restart")]]
		
		return layout
		
	
	def on_click_patrol_button(self, start, end):
		self.player.place_ship(Patrol(start,end))
		
	def on_click_submarine_button(self, start, end):
		self.player.place_ship(Submarine(start, end))
		
	def on_click_destroyer_button(self, start, end):
		self.player.place_ship(Destroyer(start, end))
		
	def on_click_battleship_button(self, start, end):
		self.player.place_ship(Battleship(start, end))
		
	def on_click_carrier_button(self, start, end):
		self.player.place_ship(Carrier(start, end))

def main():

	game = Game()
	layout = game.create_layout()
	window = sg.Window("Battleship", layout, icon = "assets/battleship.ico", margins = (30, 30))
	
	SHIP_NAMES = ["patrol", "submarine", "destroyer", "battleship", "carrier"]
	
	wait = 0 # Forces the player to perform 2 actions. There is a better way to do this, but idk how yet. 
	startcoord = -1
	endcoord = -1
	
	#Event Loop:
	while True:
		event, values = window.read()
		
		# event = the string that represents the key of a button pressed.
		if event == sg.WIN_CLOSED or event == "Exit Game":
			# If user chooses to exit the game
			break
		elif event == "New Game":
			game = Game()
			window = sg.Window("Battleship", game.create_layout(), icon = "assets/battleship.ico", margins = (30, 30))
			print("New Game Pressed")
		elif event == "How To Play":
			# Instructions on how to play (we can remove this)
			print("Help Pressed")
		elif event == "confirm" and wait == 0:
			# Placed Ships
			game.next_turn() # TODO: raises an exception MUST be caught
		else:
			print(event)
			if game.get_turn() == "position": # If turn is for placing ships. 
				
				if wait == 2 and "Player" in event:
					startcoord = eval(event.replace("Player ", ""))
					wait -= 1
				elif wait == 1 and "Player" in event:
					endcoord = eval(event.replace("Player ", ""))
					wait = 0
					
					try: 
						eval(clicked + str(startcoord) + "," + str(endcoord) + ")")
						for button_label in SHIP_NAMES: # Enable all ship placement buttons. 
							window.FindElement(button_label).Update(disabled=False)
					except(InvalidShipException):
						print("exception thrown, halt program") # Temporary action. 
					
					window.close()
					layout = game.update_ui()
					window = sg.Window("Battleship", layout, icon = "assets/battleship.ico", margins = (30, 30))
					
				elif event in SHIP_NAMES:
					for button_label in SHIP_NAMES: # Disable all ship placement buttons. 
						window.FindElement(button_label).Update(disabled=True)
					wait = 2
					clicked = "game.on_click_" + event + "_button("
					print("made it here")
		
		
			# TODO: Add Turn based event check
			#  [] Ship Placement Turn (AI Does in background)
			#  [] Player Goes first, Turn based
			#  [] Refreshes board layout after turn taken
			# Reminders: MUST CATCH EXCEPTIONS
			
		'''
		elif "Enemy" in event:
			coords = eval(event.replace("Enemy ", ""))
			enemy.fire(coords,enemyFleet)
		'''	
	window.close()

main()
