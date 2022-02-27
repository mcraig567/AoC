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
	left = math.floor(number/2)
	right = math.ceil(number/2)

	return "".join(["[", str(left), ",", str(right), "]"])

def get_index_to_split(full_string):
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
	number = []
	for i in range(index, len(full_string)):
		if full_string[i] not in ["[", "]", ","]:
			number.append(full_string[i])
		else:
			return "".join(number)

	return ''.join(number)

def get_pair_total_length(full_string, index):
	i = index
	while full_string[i] != "]":
		i += 1

	return i - index

def find_pair_to_explode(full_string):
	""" Returns the start index of first pair that need to be exploded"""
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
	
	#print(segments_to_join)

	return "".join(segments_to_join)

def reduce_line(full_string):
	explode_pair_start = find_pair_to_explode(full_string)
	split_string_start, num_to_split = get_index_to_split(full_string)

	while explode_pair_start or split_string_start:
		while explode_pair_start:
			full_string = explode_pair(full_string, explode_pair_start)
			explode_pair_start = find_pair_to_explode(full_string)
			#print("After Explode: ", full_string)
			#print()

		split_string_start, num_to_split = get_index_to_split(full_string)
		while split_string_start:
			full_string = run_split(full_string, split_string_start, num_to_split)
			#print("After Split: ", full_string)
			#print()

			explode_pair_start = find_pair_to_explode(full_string)
			if explode_pair_start:
				break

			split_string_start, num_to_split = get_index_to_split(full_string)

	return full_string

def get_magnitude_location(full_string):
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
	pair = full_string[index[0] + 1: index[1]]

	left, right = pair.split(",")

	new_val = 3 * int(left) + 2 * int(right)

	segments_to_join = [full_string[:index[0]], str(new_val), full_string[index[1] + 1:]]

	return "".join(segments_to_join)


		

### End Helper Functions ###

start = timeit.default_timer()

#test_string = "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"

#print(test_string[21])
#print(get_full_number(test_string, 21))

reduced_line = ""
for line in lines:
	if reduced_line == "":
		reduced_line = line
		#print("Initial Line:" , reduced_line)
	else:
		reduced_line = "".join(["[", reduced_line, ",", line, "]"])
		#print("After Addition: ", reduced_line)
	reduced_line = reduce_line(reduced_line)
	#print("Reduced: ", reduced_line)
	#print()

print("Final Sum: ", reduced_line)

reduce_location = get_magnitude_location(reduced_line)
while reduce_location:
	#print(reduce_location)
	reduced_line = apply_magnitude_calc(reduced_line, reduce_location)
	reduce_location = get_magnitude_location(reduced_line)
	#print(reduced_line)

print("Magnitude: ", reduced_line)
stop = timeit.default_timer()

print('Time: ', stop - start)
