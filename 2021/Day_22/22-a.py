import timeit
import math
import copy
import itertools

lines = []
with open("Input.txt", "r") as inputFile:
	for line in inputFile:
		all_combinations = []
		switch, params = line.split(" ")
		ranges = params.split(",")
		for dim in ranges:
			dim = dim[2:]
			start, stop = dim.split("..")

			# Only care about -50 to 50 in each direction
			if int(start) < -50:
				start = -50

			if int(stop) > 50:
				stop = 50

			new_list = list(range(int(start), int(stop) + 1))
			all_combinations.append(new_list)

		all_combinations = list(itertools.product(*all_combinations))
		lines.append((switch, all_combinations))

### Problem Parameters ###

### End Problem Parameters ###

### Helper Functions ###

### End Helper Functions ###

start = timeit.default_timer()

cubes_on = 0 # Runnine total so that we don't need to sum the dictionary at the end
cubes = {} # Key = (x, y, z), Value = 1 if on, 0 if false

for line in lines:
	for cube in line[1]:
		state = cubes.get(cube, None)

		# If cube is on and needs to be turned off
		if state == 1 and line[0] == "off":
			cubes[cube] = 0
			cubes_on -= 1

		# If cube is known and off, and needs to be turned on
		elif state == 0 and line[0] == "on":
			cubes[cube] = 1
			cubes_on += 1

		# If the cube has never been on, and needs to be turned on
		elif state == None and line[0] == "on":
			cubes[cube] = 1
			cubes_on += 1

stop = timeit.default_timer()
print("CUBES:", cubes_on)

print('Time: ', stop - start)
