import timeit
import copy
from heapq import heappush, heappop, heapify

# Each entry of risk_levels should be it's own dictionary
# Entry (i,j) = {
# 	id: (i,j)	
# 	risk: risk,
# 	shortest_path: 999999,
# 	visited: False,
#	parent: None
# }

risk_levels = {}
shortest_to_create = {}  # For creating a dict of distances (For debugging)
MAX_ROW = 0
MAX_COL = 0

with open("Input.txt", "r") as inputFile:
	row = 0
	for line in inputFile:
		column = 0
		for risk in line[:-1]:
			location = (row, column)

			# Prep dictionaries for Dijkstra
			risk_levels[location] = {
				"id" : (row, column),
				"risk" : int(risk),
				"shortest_path" : 999999,
				"visited" : False,
				"parent" : None
			}

			if column > MAX_COL:
				MAX_COL = column

			column += 1

		if row > MAX_ROW:
			MAX_ROW = row

		row += 1

### Problem Parameters ###

class PQueue:
	def __init__(self):
		self.queue = []

	def __str__(self):
		return " ".join([(str(i["id"]) + " - " + str(i["shortest_path"]) + ", ") for i in self.queue])

	def isEmpty(self):
		return len(self.queue) == 0

	def parent(self, i):
		return int((i-1)/2)

	def insert(self, newVal): # newVal = { id:, risk:, shortest_path:, visited:, parent: }
		self.queue.append(newVal)
		i = len(self.queue) - 1

		self.bubbleDown(i)

	def decreaseValue(self, i, new_val):
		self.queue[i]["shortest_path"] = new_val

		self.bubbleDown(i)

	def bubbleDown(self, i):
		movingVal = self.queue[i]["shortest_path"]

		while i != 0 and self.queue[self.parent(i)]["shortest_path"] > movingVal:
			self.queue[i], self.queue[self.parent(i)] = self.queue[self.parent(i)], self.queue[i]
			i = self.parent(i)

	def maintainHeap(self, i):
		smallest = i
		leftIndex = (2 * i) + 1
		rightIndex = (2 * i) + 2

		if leftIndex < len(self.queue) and self.queue[smallest]["shortest_path"] > self.queue[leftIndex]["shortest_path"]:
			smallest = leftIndex

		# If right child is smaller than left child, move to right side
		if rightIndex < len(self.queue) and self.queue[smallest]["shortest_path"] > self.queue[rightIndex]["shortest_path"]:
			smallest = rightIndex

		if smallest != i:
			self.queue[i], self.queue[smallest] = self.queue[smallest], self.queue[i]
			self.maintainHeap(smallest)

	def getMin(self):
		val = self.queue[0]
		self.queue[0] = self.queue[-1]
		self.queue.pop()
		self.maintainHeap(0)

		return val

### End Problem Parameters ###

### Helper Functions ###

def get_neighbours(location, risk_dict):
	"""Returns list of dict entries that are 'beside' the original node"""
	row = location[0]
	col = location[1]
	neighbour_list = []

	# Check up, down, left, right and add to neighbours dict 
	above = risk_dict.get((row - 1, col), None)
	if above:
		neighbour_list.append(above)

	right = risk_dict.get((row, col + 1), None)
	if right:
		neighbour_list.append(right)

	left = risk_dict.get((row, col - 1), None)
	if left:
		neighbour_list.append(left)

	below = risk_dict.get((row + 1, col), None)
	if below:
		neighbour_list.append(below)

	return neighbour_list

def check_neighbours(location, neighbours, queue):
	"""
		Determines if any neighbouring locations can be accessed by current
		location using a shorter path than current "shortest path". Modifies
		dictionary entries of risk_level

		Inputs: location is a dictionary entry from risk_levels
				neighbours are a list of dictionary entries from risk_levels
				queue is a priority queue for any known locations

		Outputs: returns True once complete. 
	"""
	
	for neighbour in neighbours:
		if not neighbour["visited"]:
			risk = neighbour["risk"]
			distance = location["shortest_path"] + risk

			if distance < neighbour["shortest_path"]:

				# We found a shorter path - update priority queue and distances
				neighbour["shortest_path"] = distance
				neighbour["parent"] = location["id"]
				shortest_to_create[neighbour["id"]] = distance
				queue.insert(neighbour)

	return True

def print_shortest(shortest_dict):
	"""	
		Debugging function. Prints out the grid with the current shortest
		paths to each node.
	"""
	for i in range(MAX_ROW + 1):
		for j in range(MAX_COL + 1):
				distance = shortest_dict.get((i,j), 999999)
				if isinstance(distance, dict):
					distance = distance["shortest_path"]

				print("{:" "<2d}".format(distance), end = " ")
		print()

	print()

def expand_map(risk_levels, max_row, max_col):
	"""
		Takes an existing grid and creates a new grid 5x larger in both x and y
		directions. Every "risk" level increases by 1 for each step right or down

		Inputs: risk_levels is the original dictionary to be multiplied
				max_row is the number of rows in the grid of risk_levels
				max_col is the number of columns in the grid of risk_levels

		Outputs: Returns the new grid as a dictionary. Keys and values keep the
				same format as the original dictionary.
	"""
	
	new_risks = {}

	for entry in risk_levels:
		risk = risk_levels[entry]["risk"]
		row = entry[0]
		col = entry[1]

		row_add = 0
		for i in range(5):
			col_add = 0
			for j in range(5):
				loc_risk = risk + i + j
				lower_risk = loc_risk % 10

				if lower_risk != loc_risk:
					lower_risk += 1

				new_risks[(row + row_add, col + col_add)] = {
					"id": (row + row_add, col + col_add),
					"risk":	lower_risk,
					"shortest_path": 999999,
					"visited": False,
					"parent": None
				}
				
				if col + col_add > new_risks.get("max_col", 0):
					new_risks["max_col"] = col + col_add
				
				col_add += max_col

			if row + row_add > new_risks.get("max_row", 0):
				new_risks["max_row"] = row + row_add

			row_add += max_row

	return new_risks


### End Helper Functions ###

start = timeit.default_timer()

# Expand map 5x each direction for part b, reset limits for print debugging
large_map = expand_map(risk_levels, MAX_ROW + 1, MAX_COL + 1)
MAX_ROW = large_map["max_row"]
MAX_COL = large_map["max_col"]
large_map.pop("max_row")
large_map.pop("max_col")

beginning = (0,0)
ending = (MAX_ROW, MAX_COL)
location = large_map[beginning]
large_map[beginning]["shortest_path"] = 0

# Initiate priority queue
shortest_queue = PQueue()
shortest_queue.insert(large_map[beginning])

# Use Dijkstra to determine shortest path to end
while not shortest_queue.isEmpty():
	location = shortest_queue.getMin()

	# Adjust neighbouring locations
	neighbours = get_neighbours(location["id"], large_map)
	check_neighbours(location, neighbours, shortest_queue)
	location["visited"] = True

	if location["id"] == ending:
		print("Shortest Distance to end: ", large_map[ending]["shortest_path"])
	
print("Done all nodes")
print("Shortest Distance to end: ", large_map[ending]["shortest_path"])

""" Uncomment if you want to see the path """
"""print_shortest(shortest_to_create)
loc = ending
path = []
while loc:
	#print(parents[loc])
	path.append(loc)
	loc = parents[loc]
	
for i in range(MAX_ROW + 1):
	for j in range(MAX_COL + 1):
		if (i,j) in path:
			print("#", end = "")
		else:
			print("-", end = "")
			#print(large_map[(i,j)], end = " ")
	print()"""

stop = timeit.default_timer()

print('Time: ', stop - start)
