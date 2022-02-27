import timeit
import copy
import math

instructions = []
with open("Input.txt", "r") as inputFile:
	for line in inputFile:
		line = line.split(" ")
		line[-1] = line[-1][:-1]
		instructions.append(line)
		
### Problem Parameters ###

min_serial = "11111111111111"
max_serial = "99999999999999"

valid_vars = ["w", "x", "y", "z"]

### End Problem Parameters ###

### Helper Functions ###

def inc_serial(serial, index):
	new_val = int(serial[index]) + 1
	
	# If a number passes 9, reset all values to the right of it to 1
	if new_val == 10:
		new_serial_list = [serial[:index]]
		for i in range(index, len(serial)):
			new_serial_list.append("1")

		new_serial = "".join(new_serial_list)
		return inc_serial(new_serial, index - 1)

	# Otherwise return string with value increased by 1
	return "".join([serial[:index], str(new_val), serial[index + 1:]])

def dec_serial(serial, index):
	new_val = int(serial[index]) - 1

	# If a number reaches 0, reset all values to the right of it to 9
	if new_val == 0:
		new_serial_list = [serial[:index]]
		for i in range(index, len(serial)):
			new_serial_list.append("9")

		new_serial = "".join(new_serial_list)
		return dec_serial(new_serial, index - 1)

	# Otherwise return string with value decreased by 1
	return "".join([serial[:index], str(new_val), serial[index + 1:]])

def add(a, b):
	return a + b

def mul(a, b):
	return a * b

def div(a, b):
	if b == 0:
		return False
	
	return math.floor(a / b)

def mod(a, b):
	if a < 0 or b <= 0:
		return False

	return a % b

def eql(a, b):
	if a == b:
		return 1
	return 0

### End Helper Functions ###

start = timeit.default_timer()

serial = max_serial
input_index = 0
variables = {}
i = 0

while serial != min_serial:
	if i % 50000 == 0:
		print(serial)

	for line in instructions:
		
		# Add the next number of the serial into the instructions
		if line[0] == "inp":
			variables[line[1]] = int(serial[input_index])
			input_index += 1

		# No new input, modify existing variables instead
		else:
			a = variables.get(line[1], 0)
			if line[2] in valid_vars:
				b = variables.get(line[2], 0)
			else:
				b = int(line[2])

		if line[0] == "add":
			variables[line[1]] = add(a, b)
		elif line[0] == "mul":
			variables[line[1]] = mul(a, b)
		elif line[0] == "div":
			variables[line[1]] = div(a, b)
		elif line[0] == "mod":
			variables[line[1]] = mod(a, b)
		elif line[0] == "eql":
			variables[line[1]] = eql(a, b)

	if variables["z"] == 0:
		print("VALID: ", serial)

	serial = dec_serial(serial, len(serial) - 1)
	input_index = 0
	variables = {}
	i += 1
			
stop = timeit.default_timer()

print('Time: ', stop - start)
