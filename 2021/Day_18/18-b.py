import timeit
import math
import copy

lines = []
with open("Input.txt", "r") as inputFile:
	for line in inputFile:
		lines.append(line[:-1])

### Problem Parameters ###

### End Problem Parameters ###

### Helper Functions ###

def split_number(number):
	""" Splits an integer into a new snailfish number.
	
		Inputs: number is any integer

		Returns: a string in the form [x,y] where is number/ 2 rounded down
		and y is number/2 rounded up	
	"""
	left = math.floor(number/2)
	right = math.ceil(number/2)

	return "".join(["[", str(left), ",", str(right), "]"])

def get_index_to_split(full_string):
	""" Determines where in the string the first split operation can occur.
		Returns None if there are no values that need to be split
	
		Inputs: full_string is a string in the form of snailfish addition

		Returns: start is the index in full_string where the number starts. 
		Number is the value that is being split, returned as a string. Returns
		None for both start and number if there are no values to be split.	
	"""
	number = ""
	start = None
	for i in range(len(full_string)):
		if full_string[i] not in ["[", "]", ","]:
			if not start:
				start = i

			number = number + full_string[i]

			if int(number) >= 10:
				return start, number

		else:
			number = ""
			start = None

	return None, None

def run_split(full_string, index, number):
	""" Applies a split operation to the string at the given index. Requires
		that the given index is the start of a number

		Inputs: full_string is a string in the form of snailfish addition.
		Index is the location in full_string where the number to be split starts.
		Number is the number (as a string) that is being split.
	
		Returns: A new string with the split operation completed.
	"""
	new_pair = split_number(int(number))

	strings_to_join = []
	strings_to_join.append(full_string[:index])
	strings_to_join.append(new_pair)
	strings_to_join.append(full_string[index + len(number):])

	return "".join(strings_to_join)

def find_next_left_number_index(full_string, index):
	""" Check string for cleset number to the left of current index. 
		Returns index of number within the string. Returns None if no numbers
		to the left of current index	
	"""
	for i in range(index - 1, 0, -1):
		if full_string[i] not in ["[", "]", ","]:
			return i

	return None

def get_full_left_number(full_string, index):
	""" Determines the entire number that crosses a given rightmost location in full_string.
		For example, if full_string[index] = 0, the full number may be 10. Requires that
		full_string[index] is a 'number'

		Inputs: full_string is a string in the form of snailfish addition.
		Index is the rightmost index of a number

		Returns: A string with the entire number that crosses full_string[index]
	"""
	number = []
	for i in range(index, 0, -1):
		if full_string[i] not in ["[", "]", ","]:
			number.append(full_string[i])
		else:
			number.reverse()
			return "".join(number)

	number.reverse()

	return ''.join(number.reverse())

def find_next_right_number_index(full_string, index):
	""" Check string for cleset number to the right of current index. 
		Returns index of number within the string. Returns None if no numbers
		to the right of current index	
	"""
	for i in range(index + 1, len(full_string)):
		if full_string[i] not in ["[", "]", ","]:
			return i

	return None

def get_full_right_number(full_string, index):
	""" Determines the entire number that crosses a given leftmost location in full_string.
		For example, if full_string[index] = 1, the full number may be 10. Requires that
		full_string[index] is a 'number'.

		Inputs: full_string is a string in the form of snailfish addition.
		Index is the leftmost index of a number

		Returns: A string with the entire number that crosses full_string[index]
	"""
	number = []
	for i in range(index, len(full_string)):
		if full_string[i] not in ["[", "]", ","]:
			number.append(full_string[i])
		else:
			return "".join(number)

	return ''.join(number)

def get_pair_total_length(full_string, index):
	""" Determines the entire length of a snailfish number pair.
		
		Inputs: full_string is a string in the form of snailfish addition.
		Index is the location of the start of the pair who's length is being
		calculated

		Returns the length of the pair as an integer. Open and closing 
		brackets are included in the total length 
	"""
	i = index
	while full_string[i] != "]":
		i += 1

	return i - index

def find_pair_to_explode(full_string):
	""" Determines where in the string the first explode operation can occur.
		Returns None if there are no pairs that need to be exploded
	
		Inputs: full_string is a string in the form of snailfish addition

		Returns: The index in full_string where the pair starts (the open bracket). 
		Returns None if there are no pairs to explode.	
	"""
	depth = 0
	for i in range(len(full_string)):
		if full_string[i] == "[":
			depth += 1
			if depth > 4:
				return i

		if full_string[i] == "]":
			depth -= 1

	return None

def explode_pair(full_string, index):
	""" Performs an explode operation on a specified pair. Requires that 
		full_string[index] is the opening bracket of a snailfish number pair.

		Inputs: full_string is a string in the form of snailfish addition.
		Index is the location of the start of the pair which is being exploded

		Returns: A new string with the explode operation completed.	
	"""
	# Check length of pair (in case of unexploded double digit numbers)	
	pair_end = index + get_pair_total_length(full_string, index)
	left_num_index = find_next_left_number_index(full_string, index)
	right_num_index = find_next_right_number_index(full_string, pair_end)

	pair = full_string[index + 1 : pair_end]
	left, right = pair.split(",")
	left = int(left)
	right = int(right)

	segments_to_join = []
	if left_num_index:
		left_num = int(get_full_left_number(full_string, left_num_index))
		new_left = left_num + left
		segments_to_join.append(full_string[:left_num_index - len(str(left_num)) + 1])
		segments_to_join.append(str(new_left))
		segments_to_join.append(full_string[left_num_index + 1 : index])
	else:
		segments_to_join.append(full_string[:index])

	segments_to_join.append("0")

	if right_num_index:
		right_num = int(get_full_right_number(full_string, right_num_index))
		new_right = right_num + right
		segments_to_join.append(full_string[pair_end + 1:right_num_index])
		segments_to_join.append(str(new_right))
		segments_to_join.append(full_string[right_num_index + len(str(right_num)):])
	else:
		segments_to_join.append(full_string[pair_end + 1:])

	return "".join(segments_to_join)

def reduce_line(full_string):
	""" Performs explode and split operations to reduce a snailfish number.
		Continues until no explode or split operations can be performed.

		Inputs: full_string is a string in the form of snailfish addition.

		Returns: A new string with the explode and split operations completed.
	"""
	explode_pair_start = find_pair_to_explode(full_string)
	split_string_start, num_to_split = get_index_to_split(full_string)

	while explode_pair_start or split_string_start:
		while explode_pair_start:
			full_string = explode_pair(full_string, explode_pair_start)
			explode_pair_start = find_pair_to_explode(full_string)

		split_string_start, num_to_split = get_index_to_split(full_string)
		while split_string_start:
			full_string = run_split(full_string, split_string_start, num_to_split)

			explode_pair_start = find_pair_to_explode(full_string)
			if explode_pair_start:
				break

			split_string_start, num_to_split = get_index_to_split(full_string)

	return full_string

def get_magnitude_location(full_string):
	""" Determines where in the string a magnitude calculation can occur.
		Returns None if there are no pairs that require a magnitude calculation
	
		Inputs: full_string is a string in the form of snailfish addition

		Returns: A tuple in the form (start, end) of the pair that can have a
		magnitude calculation performed on it. Start is the open bracket, and
		end is the close bracket. Returns None if there are no pairs that
		require a magnitude calculation.
	"""
	for i in range(len(full_string)):
		if full_string[i] == "[":
			start = i
			open = True

		if full_string[i] == "]":
			close = i

			if open:
				return (start, close)

			open = False

	return None

def apply_magnitude_calc(full_string, index):
	""" Performs a magnitude calculation on a string at the given start index.
		Requires that full_string[index] is the start of a valid snailfish pair
		with two regular numbers

		Inputs: full_string is a string in the form of snailfish addition
		Index is the starting location of a snailfish number pair.

		Returns: A new string with the magnitude calculation completed.
	
	"""
	pair = full_string[index[0] + 1: index[1]]

	left, right = pair.split(",")

	new_val = 3 * int(left) + 2 * int(right)

	segments_to_join = [full_string[:index[0]], str(new_val), full_string[index[1] + 1:]]

	return "".join(segments_to_join)

def run_full_magnitude(full_string):
	""" Performs magnitude calculations to reduce a snailfish number.
		Continues until no magnitude calculations can be performed.

		Inputs: full_string is a string in the form of snailfish addition.

		Returns: A new string with all magnitude operations completed.
	"""
	reduce_location = get_magnitude_location(full_string)
	while reduce_location:
		full_string = apply_magnitude_calc(full_string, reduce_location)
		reduce_location = get_magnitude_location(full_string)

	return full_string

### End Helper Functions ###

start = timeit.default_timer()

score_max = 0
for i in range(len(lines)):
	for j in range(len(lines)):
		if i != j:
			added_line = "".join(["[", lines[i], ",", lines[j], "]"])
			reduced_line = reduce_line(added_line)
			magnitude = int(run_full_magnitude(reduced_line))

			if magnitude > score_max:
				score_max = magnitude

print("Max score is :", score_max)

stop = timeit.default_timer()

print('Time: ', stop - start)
