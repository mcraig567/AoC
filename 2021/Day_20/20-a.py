import timeit
import math
import copy

lines = []
with open("Input.txt", "r") as inputFile:
	for line in inputFile:
		if len(line) == 513:
			img_enhc_alg = line[:-1]

		elif len(line) > 1:
			lines.append(line[:-1])
	
# Create a dictionary to allow for quick lookups and lookups of
# non-existant nodes
pixels = {}
for i in range(len(lines)):  # i = row
	for j in range(len(lines[i])):
		pixel = lines[i][j]
		if pixel == "#":
			pixels[(i, j)] = "1"

		else:
			pixels[(i,j)] = "0"

# Add in the boundaries of the current grid [min, max]
pixels["row"] = [0, len(lines)]
pixels["col"] = [0, len(lines[i])]

### Problem Parameters ###

### End Problem Parameters ###

### Helper Functions ###

def get_surrounding_bin_string(location, pixels, not_found):
	""" Returns a binary string of the 9 pixels surrounding a pixel, starting
		in the top left and going right, then middle left, then bottom left.
		Any pixels that currently don't exist are assigned a value specified
		in the inputs
		
		Requires: The location of the middle pixel in the format (row, col).
		pixels is a dictionary of each currently existing pixel. Key is a pixel
		in the form (row, col), value is a "1" if bright, "0" if dark. not found
		is the value returned when a key is not found

		Returns: A string of 0's and 1's representing the pixel's surrounding
		pixels	
	"""
	row = location[0]
	col = location[1]

	str_to_join = []

	# Get top row
	top_left = pixels.get((row - 1, col - 1), not_found)
	str_to_join.append(top_left)

	top_center = pixels.get((row - 1, col), not_found)
	str_to_join.append(top_center)
	
	top_right = pixels.get((row - 1, col + 1), not_found)
	str_to_join.append(top_right)

	# Get middle row
	mid_left = pixels.get((row, col - 1), not_found)
	str_to_join.append(mid_left)

	mid_center = pixels.get((row, col), not_found)
	str_to_join.append(mid_center)

	mid_right = pixels.get((row, col + 1), not_found)
	str_to_join.append(mid_right)	

	# Get bottom row
	bot_left = pixels.get((row + 1, col - 1), not_found)
	str_to_join.append(bot_left)

	bot_center = pixels.get((row + 1, col), not_found)
	str_to_join.append(bot_center)

	bot_right = pixels.get((row + 1, col + 1), not_found)
	str_to_join.append(bot_right)

	return "".join(str_to_join)

def convert_bin_string_to_dec(word):
	""" Converts a string of 1's and 0's into a decimal
	
		Requires: word is a string of 1's and 0's

		Returns: an int of the input word converted into decimal
	"""
	counter = 0
	dec_num = 0
	while word:
		digit = int(word[-1])
		dec_num += digit * (2 ** counter)

		word = word[:-1]
		counter += 1

	return dec_num

def perform_image_enhance(pixels, algorithm, iteration):
	""" Creates a new dictionary of all known pixels, based on the existing
		pixel dictionary and the image enhancement algorithm. Key in the 
		new dictionary is a pixel in form (row, col), and value is "1" if it
		is a light pixel, "0" otherwise.

		Requires: pixels is a dictionary of all currently known pixels, in the
		same format as described above. Algorithm is a string of "#" and "."
		describing the instructions for each pixel currently. Iteration is the
		number of turns that have taken place so far

		Returns: a new dictionary with all old pixels updated, and any newly
		discovered pixels.	
	"""

	row_boundaries = pixels["row"]
	col_boundaries = pixels["col"]

	# Determine the value of any pixels that will be discovered
	# Note that undiscovered is not always dark, in the case of algorithm[0]
	# being a #, all pixels surrounded by dark pixels will turn on.
	
	if iteration % 2 == 1 or algorithm[0] == ".":
		not_found = algorithm[0]
	else:
		not_found = algorithm[-1]

	if not_found == "#":
		not_found = "1"
	else:
		not_found = "0"	

	# If we have a 3x3 grid, will need to check the pixels on every edge, creating a 5x5 grid

	new_pixels = {}
	for i in range(row_boundaries[0] - 1, row_boundaries[1] + 1):
		for j in range(col_boundaries[0] - 1, col_boundaries[1] + 1):
			bin_str = get_surrounding_bin_string((i, j), pixels, not_found)
			dec_index = convert_bin_string_to_dec(bin_str)
			pixel_val = algorithm[dec_index]

			if pixel_val == "#":
				new_pixels[(i, j)] = "1"
			else:
				new_pixels[(i, j)] = "0"

	
	new_pixels["row"] = [row_boundaries[0] - 1, row_boundaries[1] + 1]
	new_pixels["col"] = [col_boundaries[0] - 1, col_boundaries[1] + 1]

	return new_pixels

def get_pixel_count(pixels):
	""" Determines the number of light pixels in the input dictionary.

		Requires: pixels is a dictionary of individual pixels where a
		light pixel has a value of "1" (as a string)

		Returns: an int representing the number of light pixels
	"""

	count = 0
	for pixel in pixels.values():
		if pixel == "1":
			count += 1

	return count

def print_pixels(pixels, not_found):
	""" To help with debugging, prints a grid of all current pixels
		with a 2 unit buffer on each edge
	"""
	row_boundaries = pixels["row"]
	col_boundaries = pixels["col"]

	count = 0
	for i in range(row_boundaries[0], row_boundaries[1]):
		for j in range(col_boundaries[0], col_boundaries[1]):			
			pixel = pixels.get((i,j), not_found)

			if pixel == "1":
				pixel = "#"
			elif pixel == "0":
				pixel = "."
			else:
				pixel = not_found

			if pixel == "#":
				count += 1

			print("{:<2}".format(pixel), end = "")
		print()
	print("Printed", count, "#s")

### End Helper Functions ###

start = timeit.default_timer()

print("Starting:", get_pixel_count(pixels), "pixels")

for i in range(50):

	if i % 2 == 0:
		not_found = "#"
	else:
		not_found = "."
	pixels = perform_image_enhance(pixels, img_enhc_alg, i)

print("There are", get_pixel_count(pixels), "pixels")

stop = timeit.default_timer()

print('Time: ', stop - start)
