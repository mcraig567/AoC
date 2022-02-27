import timeit
import copy
import math

all_cukes = {} # Key = (row, column), Value = Type of cuke

MAX_COL = 0
MAX_ROW = 0

with open("Input.txt", "r") as inputFile:
	row = 0
	for line in inputFile:
		for col in range(len(line)):
			loc = (row, col)
			if line[col] == "v":
				all_cukes[loc] = "v"
			elif line[col] == ">":
				all_cukes[loc] = ">"

		MAX_ROW = row
		row += 1

		MAX_COL = max(MAX_COL, len(line) - 2)
		
all_cukes["max_col"] = MAX_COL
all_cukes["max_row"] = MAX_ROW
		
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
					(all_cukes.get((0, cuke[1]), True) != "v" and move_check(all_cukes, (0, cuke[1]))) and\
					(all_cukes.get((0, cuke[1] - 1), True) != ">" or not move_check(all_cukes, (0, cuke[1] - 1))):
				to_move.append(cuke)

		# Check bottom left corner
		elif cuke == (all_cukes["max_row"], 0):
			if all_cukes.get(cuke, False) == ">" and all_cukes.get((cuke[0], cuke[1] + 1), True) == True:
				to_move.append(cuke)
			
			elif all_cukes.get(cuke) == "v" and \
					(all_cukes.get((0, 0), True) != "v" and move_check(all_cukes, (0, 0))) and \
					(all_cukes.get((0, all_cukes["max_col"])) != ">" or not move_check(all_cukes, (0, all_cukes["max_col"]))):
				to_move.append(cuke)

		# Check rest of right edge
		elif cuke[1] == all_cukes["max_col"]: 
			if all_cukes.get(cuke, False) == ">" and all_cukes.get((cuke[0], 0), True) == True:
				to_move.append(cuke)

			elif all_cukes.get(cuke, False) == "v" and \
					(all_cukes.get((cuke[0] + 1, cuke[1]), True) != "v" and move_check(all_cukes, (cuke[0] + 1, cuke[1]))) and \
					(all_cukes.get((cuke[0] + 1, cuke[1] - 1), True) != ">" or not move_check(all_cukes, (cuke[0] + 1, cuke[1] - 1))):
				to_move.append(cuke)

		# Check rest of bottom edge
		elif cuke[0] == all_cukes["max_row"]:
			if all_cukes.get(cuke, False) == ">" and all_cukes.get((cuke[0], cuke[1] + 1), True) == True:
				to_move.append(cuke)

			elif all_cukes.get(cuke, False) == "v" and \
					(all_cukes.get((0, cuke[1]), True) != "v" and move_check(all_cukes, (0, cuke[1]))) and \
					(all_cukes.get((0, cuke[1] - 1), True) != ">" or not move_check(all_cukes, (0, cuke[1] - 1))):
				to_move.append(cuke)

		# Check rest of left edge
		elif cuke[1] == 0:
			if all_cukes.get(cuke, False) == ">" and all_cukes.get((cuke[0], cuke[1] + 1), True) == True:
				to_move.append(cuke)

			elif all_cukes.get(cuke, False) == "v" and \
					(all_cukes.get((cuke[0] + 1, 0), True) != "v" and move_check(all_cukes, (cuke[0] + 1, 0))) and \
					(all_cukes.get((cuke[0] + 1, all_cukes["max_col"]), True) != ">" or not move_check(all_cukes, (cuke[0] + 1, all_cukes["max_col"]))):
				to_move.append(cuke)

		# Check rest of cukes
		else:
			if all_cukes.get(cuke, False) == ">" and all_cukes.get((cuke[0], cuke[1] + 1), True) == True:
				to_move.append(cuke)

			elif all_cukes.get(cuke, False) == "v" and \
					(all_cukes.get((cuke[0] + 1, cuke[1]), True) != "v" and move_check(all_cukes, (cuke[0] + 1, cuke[1]))) and \
					(all_cukes.get((cuke[0] + 1, cuke[1] - 1), True) != ">" or not move_check(all_cukes, (cuke[0] + 1, cuke[1] - 1))):

				to_move.append(cuke)

	return to_move

def move_cukes(all_cukes, to_move):
	""" Applies all of the moves that will happen this turn. Modifies the
	current dictionary with the updated cucumber locations.

	Requires: all_cukes is a dictionary where each key is a location (row, col)
	and the value is the type of cucumber in the dict. Any locations without
	a cucumber is blank. to_move is a list of locations, (row, col), that will
	move this turn.

	Returns: The initial dictionary all_cukes with the updated cucumber locations	
	"""

	# If south herd moved into a spot that contained an east cuke earlier this turn, the algorithm will move
	# if twice (When it checks the old east spot, now registers as a south cuke).
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

	return all_cukes
	
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

	if herd == ">":
		if cuke[1] == all_cukes["max_col"]:
			if all_cukes.get((cuke[0], 0), True) == True:
				return True
		else:
			if all_cukes.get((cuke[0], cuke[1] + 1), True) == True:
				return True

	elif herd == "v":
		if cuke[0] == all_cukes["max_row"]:
			if all_cukes.get((0, cuke[1]), True) == True:
				return True

		else:
			if all_cukes.get((cuke[0] + 1, cuke[1]), True) == True:
				return True

	return False

def print_grid(cukes):
	""" Print out the grid of cucumbers for debugging """
	for i in range(cukes["max_row"] + 1):
		print(f'{i:03}', end = " ")
		for j in range(cukes["max_col"] + 1):
			print(cukes.get((i,j), "."), end="")
		print()
	print()

### End Helper Functions ###

start = timeit.default_timer()

# Determine the cukes that can move from the initial state
cukes_to_move = get_original_moves(all_cukes)

# Update grid of cucumbers and determine new moves until no
# cucumbers will move the next turn
i = 0
while len(cukes_to_move) > 0:
	all_cukes = move_cukes(all_cukes, cukes_to_move)
	cukes_to_move = get_original_moves(all_cukes)

	i += 1

print("Complete in ", i + 1, "turns")
			
stop = timeit.default_timer()

print('Time: ', stop - start)
