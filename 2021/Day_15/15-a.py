import timeit
import copy

risk_levels = {}
unvisited = {}
shortest_distance = {}
shortest_to_create = {}
MAX_ROW = 0
MAX_COL = 0

with open("InputTest.txt", "r") as inputFile:
	row = 0
	for line in inputFile:
		column = 0
		for risk in line[:-1]:
			location = (row, column)

			# Prep dictionaries for Dijkstra
			risk_levels[location] = int(risk)
			unvisited[location] = True
			shortest_distance[location] = 999999

			if column > MAX_COL:
				MAX_COL = column

			column += 1

		if row > MAX_ROW:
			MAX_ROW = row

		row += 1

# We never visit the start node
shortest_distance[(0,0)] = 0

### Problem Parameters ###

### End Problem Parameters ###

### Helper Functions ###

def get_neighbours(location, risk_dict):
	"""Returns list of locations sorted from lowest to highest risk"""
	row = location[0]
	col = location[1]
	neighbours = {}

	# Check up, down, left, right and add to neighbours dict 
	above = risk_dict.get((row - 1, col), None)
	if above:
		neighbours[(row - 1, col)] = above

	right = risk_dict.get((row, col + 1), None)
	if right:
		neighbours[(row, col + 1)] = right

	below = risk_dict.get((row + 1, col), None)
	if below:
		neighbours[(row + 1, col)] = below

	left = risk_dict.get((row, col - 1), None)
	if left:
		neighbours[(row, col - 1)] = left

	# Sort by risk level and create a list of all neighbours
	neighbour_list = []
	for key in sorted(neighbours.items(), key = lambda item: item[1]):
		neighbour_list.append(key[0])

	return neighbour_list

def check_neighbours(location, risk_dict):
	edge_neighbours = get_neighbours(location, risk_dict)
	for neighbour in edge_neighbours:
		if neighbour in shortest_distance:
			risk = risk_dict[neighbour]
			distance = shortest_distance[location] + risk

			if distance < shortest_distance[neighbour]:
				shortest_distance[neighbour] = distance
				shortest_to_create[neighbour] = distance
				#print(location)
				#print_shortest(shortest_distance)

	return True

def get_smallest_unvisited(shortest_distance):
	return min(shortest_distance, key=shortest_distance.get)

def print_shortest(shortest_dict):
	for i in range(MAX_ROW + 1):
		for j in range(MAX_COL + 1):
				print("{:" "<7d}".format(shortest_dict.get((i,j), 999999)), end = " ")
		print()

	print()


### End Helper Functions ###

start = timeit.default_timer()

beginning = (0,0)
ending = (MAX_ROW, MAX_COL)
print(ending)

location = beginning	# Start at beginning
#print_shortest(shortest_distance)
#print()
while shortest_distance:

	# Adjust neighbouring locations
	check_neighbours(location, risk_levels)

	# Find value with the smallest tentative distance
	shortest_distance.pop(location)
	location = get_smallest_unvisited(shortest_distance)
	#print("setting location to ", location)
	
	if location == ending:
		print("Shortest Distance to end: ", shortest_distance[ending])
		break

print_shortest(shortest_to_create)

stop = timeit.default_timer()

print('Time: ', stop - start)
