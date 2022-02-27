import timeit
import copy
import math

all_cukes = {} # Key = (row, column), Value = Type of cuke
east_herd = [] # Each entry represents a location where an east facing cucumber is. Want sorted high-low by column eventually.
south_herd = []

MAX_COL = 0
MAX_ROW = 0

with open("Input.txt", "r") as inputFile:
	row = 0
	for line in inputFile:
		for col in range(len(line)):
			loc = (row, col)
			if line[col] == "v":
				all_cukes[loc] = "v"
				south_herd.append(loc)
			elif line[col] == ">":
				all_cukes[loc] = ">"
				east_herd.append(loc)

		MAX_ROW = row
		row += 1

		MAX_COL = max(MAX_COL, len(line) - 2)
		
all_cukes["max_col"] = MAX_COL
all_cukes["max_row"] = MAX_ROW - 1
all_cukes["changed"] = True
		
### Problem Parameters ###

### End Problem Parameters ###

### Helper Functions ###

def get_original_moves(all_cukes):
	""" Checks all cucumbers in input dictionary and determines which cukes
	will be moved in the next turn. 

	Requires: all_cukes is a dictionary where each key is a location (row, col)
	and the value is the type of cucumber in the dict. Any locations without
	a cucumber is blank.

	Returns: A list of all locations that will have a cucumber moving in the
	next turn
	"""
	to_move = []
	for cuke in all_cukes:

		# Check bottom right corner
		if cuke == (all_cukes["max_row"], all_cukes["max_col"]):
			if all_cukes.get(cuke) == ">" and all_cukes.get((cuke[0], 0), True) == True:
				to_move.append(cuke)

			elif all_cukes.get(cuke) == "v" and \
				(all_cukes.get((0, cuke[1]), True) != "v" and \
				move_check(all_cukes, (0, cuke[1]))) and\
				(all_cukes.get((0, cuke[1] - 1), True) != ">" or \
				not move_check(all_cukes, (0, cuke[1] - 1))):
				to_move.append(cuke)

		# Check bottom left corner
		elif cuke == (all_cukes["max_row"], 0):
			if all_cukes.get(cuke, False) == ">" and all_cukes.get((cuke[0], cuke[1] + 1), True) == True:
				to_move.append(cuke)
			
			elif all_cukes.get(cuke) == "v" and \
				(all_cukes.get((0, 0), True) != "v" and \
				move_check(all_cukes, (0, 0))) and \
				(all_cukes.get((0, all_cukes["max_col"])) != ">" or \
				not move_check(all_cukes, (0, all_cukes["max_col"]))):
				to_move.append(cuke)

		# Check rest of right edge
		elif cuke[1] == all_cukes["max_col"]: 
			if all_cukes.get(cuke, False) == ">" and all_cukes.get((cuke[0], 0), True) == True:
				to_move.append(cuke)

			elif all_cukes.get(cuke, False) == "v" and \
				(all_cukes.get((cuke[0] + 1, cuke[1]), True) != "v" and \
				move_check(all_cukes, (cuke[0] + 1, cuke[1]))) and \
				(all_cukes.get((cuke[0] + 1, cuke[1] - 1), True) != ">" or \
				not move_check(all_cukes, (cuke[0] + 1, cuke[1] - 1))):
				to_move.append(cuke)

		# Check rest of bottom edge
		elif cuke[0] == all_cukes["max_row"]:
			if all_cukes.get(cuke, False) == ">" and all_cukes.get((cuke[0], cuke[1] + 1), True) == True:
				to_move.append(cuke)

			elif all_cukes.get(cuke, False) == "v" and \
				(all_cukes.get((0, cuke[1]), True) != "v" and \
				move_check(all_cukes, (0, cuke[1]))) and \
				(all_cukes.get((0, cuke[1] - 1), True) != ">" or \
				not move_check(all_cukes, (0, cuke[1] - 1))):
				to_move.append(cuke)

		# Check rest of left edge
		elif cuke[1] == 0:
			if all_cukes.get(cuke, False) == ">" and all_cukes.get((cuke[0], cuke[1] + 1), True) == True:
				to_move.append(cuke)

			elif all_cukes.get(cuke, False) == "v" and \
				(all_cukes.get((cuke[0] + 1, cuke[1]), True) != "v" and \
				move_check(all_cukes, (cuke[0] + 1, cuke[1]))) and \
				(all_cukes.get((cuke[0] + 1, all_cukes["max_col"]), True) != ">" or \
				not move_check(all_cukes, (cuke[0] + 1, all_cukes["max_col"]))):
				to_move.append(cuke)

		# Check rest of cukes
		else:
			if all_cukes.get(cuke, False) == ">" and all_cukes.get((cuke[0], cuke[1] + 1), True) == True:
				to_move.append(cuke)

			elif all_cukes.get(cuke, False) == "v" and \
				(all_cukes.get((cuke[0] + 1, cuke[1]), True) != "v" and \
				move_check(all_cukes, (cuke[0] + 1, cuke[1]))) and \
				(all_cukes.get((cuke[0] + 1, cuke[1] - 1), True) != ">" or \
				not move_check(all_cukes, (cuke[0] + 1, cuke[1] - 1))):

				to_move.append(cuke)

	return to_move

def move_cukes(all_cukes, to_move):

	### Need to have east herd move first, then go through and repeat with south herd *before* checking next move spots

	new_to_move = set()
	moved_into = []

	# Move all cucumbers that will move this turn, first east then south
	for i in range(2):
		if i == 0:
			active_herd = ">"
		elif i == 1:
			active_herd = "v"

		for cuke in to_move:
			herd = all_cukes.get(cuke, True)

			if herd == active_herd and cuke not in moved_into:

				# Check bottom right corner
				if cuke == (all_cukes["max_row"], all_cukes["max_col"]):
					if herd == ">":
						new_loc = (cuke[0], 0)
					elif herd == "v":
						new_loc = (0, cuke[1])

				# Check rest of right column
				elif cuke[1] == all_cukes["max_col"]:
					if herd == ">":
						new_loc = (cuke[0], 0)
					elif herd == "v":
						new_loc = (cuke[0] + 1, cuke[1])

				# Check rest of bottom row
				elif cuke[0] == all_cukes["max_row"]:
					if herd == ">":
						new_loc = (cuke[0], cuke[1] + 1)
					elif herd == "v":
						new_loc = (0, cuke[1])

				# Any other location
				else:
					if all_cukes[cuke] == ">":
						new_loc = (cuke[0], cuke[1] + 1)

					elif all_cukes[cuke] == "v":
						new_loc = (cuke[0] + 1, cuke[1])
				
				# Update all_cukes with new cucumber location
				all_cukes[new_loc] = herd
				all_cukes.pop(cuke)

				moved_into.append(new_loc)

	# Go through the initial positions of each cuke that moved this turn,
	# and determine which cukes will move next turn

	#print_grid(all_cukes)

	for cuke in to_move:
		next_cuke_moving = get_next_move(all_cukes, cuke)
		if next_cuke_moving :
			#print("Moving cuke", cuke, "opens up", next_cuke_moving)
			new_to_move.add(next_cuke_moving)
		#else:
			#print("Moving cuke", cuke, "does not free up a new cuke")
	#print()

	# Check each new location to determine which cukes that moved this turn will
	# move again next turn
	for loc in moved_into:
		if move_check(all_cukes, loc):
			new_to_move.add(new_loc)
			#print("Cuke ", loc, "will be able to move again")
		#else:
			#print("Cuke ", loc, "will not move next turn")

	new_to_move = list(new_to_move)

	return all_cukes, new_to_move
	

def get_next_move(all_cukes, cuke):
	""" Determines which, if any, cucumbers will be able to move next turn
	as a result of this cucumber moving.

	Requires: all_cukes is a dictionary of cukes where the key is (row, col),
	and values are the herd of the cucumber in that location at this time. Cuke
	is the location to be checked
	
	Returns: a tuple (row, col) of the cucumber that can be moved next turn, or
	None if no cucumbers can move.
	"""

	# Need to check left of the spot first for east herd, then above the spot for south herd

	# Check top left corner first
	if cuke == (0, 0):
		if all_cukes.get((0, all_cukes["max_col"]), True) == ">":
			return (0, all_cukes["max_col"])
		elif all_cukes.get((all_cukes["max_row"], 0), True) == "v":
			return (all_cukes["max_col"], 0)

	# Check rest of left column
	elif cuke[1] == 0:
		if all_cukes.get((cuke[0], all_cukes["max_col"]), True) == ">":
			return (cuke[0], all_cukes["max_col"])
		elif all_cukes.get((cuke[0] - 1, 0), True) == "v":
			return (cuke[0] - 1, 0)

	# Check rest of top row
	elif cuke[0] == 0:
		if all_cukes.get((0, cuke[1] - 1), True) == ">":
			return (0, cuke[1] - 1)
		elif all_cukes.get((all_cukes["max_row"], cuke[1]), True) == "v":
			return (all_cukes["max_row"], cuke[1])
	
	# Check all other locations
	else:
		if all_cukes.get((cuke[0], cuke[1] - 1), True) == ">":
			return (cuke[0], cuke[1] - 1)
		elif all_cukes.get((cuke[0] - 1, cuke[1]), True) == "v":
			return (cuke[0] - 1, cuke[1])

	return None

def move_check(all_cukes, cuke):
	""" Checks an individual location to see if it will move in the next turn.
	
	Requires: all_cukes is a dictionary of cukes where the key is (row, col),
	and values are the herd of the cucumber in that location at this time. Cuke
	is the location to be checked

	Returns: True is the cucumber will move next turn or there is no cucumber
	at this location, False otherwise	
	"""
	herd = all_cukes.get(cuke, False)
	if herd == False:
		return True

	# East herd just need to check if spot to the right is clear
	if herd == ">":
		if cuke[1] == all_cukes["max_col"]:
			if all_cukes.get((cuke[0], 0), True) == True:
				return True
		else:
			if all_cukes.get((cuke[0], cuke[1] + 1), True) == True:
				return True

	# South herd needs to check if spot is blank and that no east herd
	# move into that spot before it moves.
	elif herd == "v":
		if cuke[0] == all_cukes["max_row"]:
			if all_cukes.get((0, cuke[1]), True) == True:
				return True

		else:
			if all_cukes.get((cuke[0] + 1, cuke[1]), True) == True:
				return True

	return False


def print_grid(cukes):
	for i in range(cukes["max_row"] + 1):
		for j in range(cukes["max_col"] + 1):
			print(cukes.get((i,j), "."), end="")
		print()
	print()

### End Helper Functions ###

start = timeit.default_timer()

cukes_to_move = get_original_moves(all_cukes)

i = 0
while len(cukes_to_move) > 0:
	if i % 100 == 0:
		print("Turn", i)
	#print_grid(all_cukes)
	change_check = False

	all_cukes, cukes_to_move = move_cukes(all_cukes, cukes_to_move)
	cukes_to_move = get_original_moves(all_cukes)

	i += 1

print("Complete in ", i, "turns")
#print_grid(all_cukes)
			
stop = timeit.default_timer()

print('Time: ', stop - start)
