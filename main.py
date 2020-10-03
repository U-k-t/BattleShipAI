import PySimpleGUI as sg # sg : simple gui
from repository.image_repository import ImageRepository
from battleship import Fleet, Ship, Grid

BOARD_SIZE = 10

class Game:

	def __init__(self):
		print("Create Game Object")

		# Constant: Menu Bar at the top. We can add other options for how we want to see stuff.
		self.menu_bar = [ ["Game", ["New Game", "Exit Game"]],
						  ["Help", ["How To Play"]]]

		# Start what the window will look like:
		self.layout = [[sg.Menu(self.menu_bar, tearoff = False, key="-MENU-")],
					   [sg.Text("Player vs. BUTTS the Battleship game AI")],
					   [sg.Image('assets/battleship.png', size=(600,200))]]

		self.player_board = [[ImageRepository.get_empty_image() for col in range(BOARD_SIZE)] for row in range(BOARD_SIZE)]
		self.enemy_board = [[ImageRepository.get_empty_image() for col in range(BOARD_SIZE)] for row in range(BOARD_SIZE)]

	def create_layout(self):
		# board layout: Player left column, enemy right column
		enemy_board_layout = self.__create_enemy_grid()
		player_board_layout = self.__create_player_grid()

		self.layout += [[sg.Column(player_board_layout),
				         sg.VSeperator(), # Line that separates the two.
				         sg.Column(enemy_board_layout)]]

		return self.layout

	def __create_player_grid(self):
		player_board_layout = [[sg.Text("Player Board:")]]
		player_board_layout += [[sg.Button('', image_data=self.player_board[row][col], button_color=(sg.theme_background_color(), sg.theme_background_color()), size = (4,2), pad=(0,0), key=(row,col)) for col in range(10)] for row in range(10)]
		return player_board_layout

	def __create_enemy_grid(self):
		enemy_board_layout = [[sg.Text("Enemy Board:")]]
		enemy_board_layout += [[sg.Button('', image_data=self.enemy_board[row][col], button_color=(sg.theme_background_color(), sg.theme_background_color()), size = (4,2), pad=(0,0), key="Enemy " + str((row,col))) for col in range(10)] for row in range(10)]
		return enemy_board_layout

def main():

	game = Game()
	window = sg.Window("Battleship", game.create_layout(), icon = "assets/battleship.ico", margins = (30, 30))
	player = Grid()
	enemy = Grid()
	fleet = Fleet()
	enemyFleet = Fleet()
	enemyFleet.addShip((1,1),(1,2),Ship(2,"Patrol"))
	enemyFleet.addShip((2,1),(2,3),Ship(3,"Submarine"))
	enemyFleet.addShip((3,1),(3,3),Ship(3,"Destroyer"))
	enemyFleet.addShip((4,1),(4,4),Ship(4,"Battleship"))
	enemyFleet.addShip((5,1),(5,5),Ship(5,"Carrier"))
	enemy.setFleet(enemyFleet.getShips())

	#Event Loop:
	while True:
		event, values = window.read()

		if event == sg.WIN_CLOSED or event == "Exit Game":
			# If user chooses to exit the game
			break
		elif event == "New Game":
			# If the user wants to start a new game
			print("New Game Pressed")
		elif event == "How To Play":
			# Instructions on how to play (we can remove this)
			print("Help Pressed")
		elif "Enemy" in event:
			coords = eval(event.replace("Enemy ", ""))
			enemy.fire(coords,enemyFleet)

	window.close()

main()
