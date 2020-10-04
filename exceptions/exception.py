# If the position that a player attempts to hit is already taken. 
class AlreadyPointTakenException(Exception):
	pass
	
# Thrown if a ship's coordinates are not valid
class InvalidShipPlacementException(Exception):
	pass

# Thrown if a ship already exists within the fleet	
class ShipAlreadyExistsException(Exception):
	pass
	
# Thrown if a ship is not created properly
class InvalidShipException(Exception):
	pass

# thrown if board is not initialized with ships. 
class BoardNotCompleteException(Exception):
	pass