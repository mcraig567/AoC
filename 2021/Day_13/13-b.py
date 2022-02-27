import timeit
import copy

dots = {} # Key = (row, column), Value = 1
folds = [] # Each entry to be (direction, position to fold at)

#For printing the grid
max_row = 0
max_col = 0

with open("Input.txt", "r") as inputFile:
	for line in inputFile:
		line = line.split(",")

		#Dot locations
		if len(line) > 1:
			row = int(line[1])
			column = int(line[0])
			dots[(row, column)] = 1

			if row > max_row:
				max_row = row
			if column > max_col:
				max_col = column

		#Folds
		elif len(line[0]) > 3:
			fold_instruction = line[0].split(" ")
			dir, value = fold_instruction[2].split("=")
			folds.append((dir, int(value)))

### Problem Parameters ###

### End Problem Parameters ###

### Helper Functions ###

#Fold up on horizontal fold (x), Fold left on vertical fold (y)

def get_affected_dots_horizontal(dots, row):
	""" Determine all dots that would be affected if a horizontal (bottom up)
		fold was applied at specified location.

		Requires: Dictionary of all dots, row where fold is applied

		Returns: List of all affected dot locations
	"""
	affected = []
	for dot in dots:
		if dot[0] > row and dots[dot] == 1:
			affected.append(dot)

	return affected

def get_affected_dots_vertical(dots, col):
	""" Determine all dots that would be affected if a 
		horizontal (right -> left) fold was applied at specified location.

		Requires: Dictionary of all dots, column where fold is applied

		Returns: List of all affected dot locations
	"""
	affected = []
	for dot in dots:
		if dot[1] > col and dots[dot] == 1:
			affected.append(dot)

	return affected

def get_new_dot_location_horizontal(dots_list, fold):
	""" Determines locations of dots after a horizontal fold (bottom up)
		fold has taken place

		Requires: List of dots that are affected by fold, row where fold
		is applied

		Returns: List of new dot locations
	"""
	new_locations = []
	for dot in dots_list:
		new_row = fold - (dot[0] - fold)
		new_locations.append((new_row, dot[1]))
	
	return new_locations

def get_new_dot_location_vertical(dots_list, fold):
	""" Determines locations of dots after a vertical fold (right -> left)
		fold has taken place

		Requires: List of dots that are affected by fold, column where fold
		is applied

		Returns: List of new dot locations
	"""
	new_locations = []	
	for dot in dots_list:
		new_col = fold - (dot[1] - fold)
		new_locations.append((dot[0], new_col))
	
	return new_locations

def remove_original_dots(dots_list, dots_dict):
	"""Modifies input dictionary to no longer include dots provided"""
	for dot in dots_list:
		dots_dict[dot] = 0

	return True

def add_new_dots(dots_list, dots_dict):
	"""Modifies input dictionary to include new dots provided in input list"""
	for dot in dots_list:
		dots_dict[dot] = 1

	return True

def print_dot_grid(dots, rows=max_row, cols=max_col):
	""" Prints a display of all active dots. By default will print full sized
		grid determined when parsing input.

		Requires input dictionary to have key format (row, col)
	"""
	for row in range(rows + 1):
		for col in range(cols + 1):
			dot = dots.get((row, col), 0)
			if dot == 1:
				dot_print = "#"
			else:
				dot_print = "."
			
			print(dot_print, end = "")
		print()

def get_max_dimensions(dots):
	""" Determine the largest row and column of exisiting dot
	
		Requires input dictionary with key format (row, col)
	"""
	max_row = 0
	max_col = 0
	for dot in dots:
		if dots[dot] == 1:
			if dot[0] > max_row:
				max_row = dot[0]
			if dot[1] > max_col:
				max_col = dot[1]

	return max_row, max_col
			
### End Helper Functions ###

start = timeit.default_timer()

# Apply folds to exisiting dictionary of dots
for fold in folds:
	if fold[0] == "y":
		affected_dots = get_affected_dots_horizontal(dots, fold[1])
		new_locations = get_new_dot_location_horizontal(affected_dots, fold[1])

	elif fold[0] == "x":
		affected_dots = get_affected_dots_vertical(dots, fold[1])
		new_locations = get_new_dot_location_vertical(affected_dots, fold[1])

	remove_original_dots(affected_dots, dots)
	add_new_dots(new_locations, dots)

# Determine new dimensions (don't want 1000 x 1000 grid) and print
rows, cols = get_max_dimensions(dots)
print_dot_grid(dots, rows, cols)

stop = timeit.default_timer()

print('Time: ', stop - start)
