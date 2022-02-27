import timeit
import copy
from heapq import heappush, heappop, heapify

risk_levels = {}
unvisited = {}
shortest_distance = {}
shortest_to_create = {}
parents = {(0,0): None}
MAX_ROW = 0
MAX_COL = 0

with open("Input.txt", "r") as inputFile:
	row = 0
	for line in inputFile:
		column = 0
		for risk in line[:-1]:
			location = (row, column)

			# Prep dictionaries for Dijkstra
			risk_levels[location] = int(risk)

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
		return " ".join([str(i[0]) for i in self.queue])

	def isEmpty(self):
		return len(self.queue) == 1

	def parent(self, i):
		return int((i)/2)

	def insert(self, newVal): # newVal = [distance, (row, col)]
		self.queue.append(newVal)
		i = len(self.queue) - 1

		while (i != 0 and self.queue[self.parent(i)][0] > self.queue[i][0]):
			self.queue[i], self.queue[self.parent(i)] = self.queue[self.parent(i)], self.queue[i]

	def decreaseValue(self, i, new_val):
		self.queue[i] = [new_val, self.queue[i][1]]
		parent_val = self.queue[self.parent(i)][0]

		while i != 0 and parent_val > new_val:
			self.queue[i], self.queue[self.parent(i)] = self.queue[self.parent(i)], self.queue[i]
			i = self.parent(i)
			parent_val = self.queue[self.parent(i)][0]

	def maintainHeap(self, i):
		smallest = i
		leftIndex = 2 * i
		rightIndex = 2 * i + 1

		if leftIndex < len(self.queue) and self.queue[smallest][0] > self.queue[leftIndex][0]:
			smallest = leftIndex

		# If right child is smaller than left child, move to right side
		if rightIndex < len(self.queue) and self.queue[smallest][0] > self.queue[rightIndex][0]:
			smallest = rightIndex

		if smallest != i:
			self.queue[i], self.queue[smallest] = self.queue[smallest], self.queue[i]
			self.maintainHeap(smallest)

	def getMin(self):
		val = self.queue[1]
		self.queue[1] = self.queue[-1]
		self.queue.pop()
		self.maintainHeap(1)

		return val

	def getIndex(self, loc):
		for i in range(len(self.queue)):
			item = self.queue[i]
			if item[1] == loc:
				return i
		return -1

	def isIn(self, loc):
		if self.getIndex(loc) == -1:
			return False
		return True	

### End Problem Parameters ###

### Helper Functions ###

def get_neighbours(location, risk_dict):
	"""
	Returns list of locations that are adjacent to current location
	"""
	row = location[0]
	col = location[1]
	neighbours = {}

	# Check up, down, left, right and add to neighbours dict 
	above = risk_dict.get((row - 1, col), None)
	if above:
		neighbours[(row - 1, col)] = above

	left = risk_dict.get((row, col - 1), None)
	if left:
		neighbours[(row, col - 1)] = left

	right = risk_dict.get((row, col + 1), None)
	if right:
		neighbours[(row, col + 1)] = right

	below = risk_dict.get((row + 1, col), None)
	if below:
		neighbours[(row + 1, col)] = below

	# Create a list and return
	neighbour_list = []
	for key in neighbours:
		neighbour_list.append(key)

	return neighbour_list

def check_neighbours(location, risk_dict, queue):
	"""
	Updates the neighbouring locations with the shortest known distance to
	them from the starting node. Modifies dictionaries

	"""
	edge_neighbours = get_neighbours(location, risk_dict)
	for neighbour in edge_neighbours:
		if neighbour in shortest_distance:
			risk = risk_dict[neighbour]
			distance = shortest_distance[location] + risk

			if distance < shortest_distance[neighbour]:
				if queue.isIn(neighbour):
					index = queue.getIndex(neighbour)
					queue.decreaseValue(index, distance)
				else:
					queue.insert([distance, neighbour])

				shortest_distance[neighbour] = distance
				shortest_to_create[neighbour] = distance
				parents[neighbour] = location

	return True

def get_smallest_unvisited(shortest_distance):
	return shortest_distance.getMin()

def print_shortest(shortest_dict):
	for i in range(MAX_ROW + 1):
		for j in range(MAX_COL + 1):
				print("{:" "<2d}".format(shortest_dict.get((i,j), 999999)), end = " ")
		print()

	print()

def expand_map(risk_levels, max_row, max_col):
	new_risks = {}

	for entry in risk_levels:
		risk = risk_levels[entry]
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

				new_risks[(row + row_add, col + col_add)] = lower_risk
				
				if col + col_add > new_risks.get("max_col", 0):
					new_risks["max_col"] = col + col_add
				
				col_add += max_col

			if row + row_add > new_risks.get("max_row", 0):
				new_risks["max_row"] = row + row_add

			row_add += max_row

	return new_risks


### End Helper Functions ###

start = timeit.default_timer()

large_map = expand_map(risk_levels, MAX_ROW + 1, MAX_COL + 1)
MAX_ROW = large_map["max_row"]
MAX_COL = large_map["max_col"]

large_map.pop("max_row")
large_map.pop("max_col")

beginning = (0,0)
ending = (MAX_ROW, MAX_COL)
location = beginning

for key in large_map:
	if key != "max_row" and key != "max_col":
		shortest_distance[key] = 999999

# We never visit the start node
shortest_distance[(0,0)] = 0

# Initiate Priority Queue
shortest_queue = PQueue()
shortest_queue.insert([0, (0,0)])

while shortest_distance:

	# Adjust neighbouring locations
	check_neighbours(location, large_map, shortest_queue)

	# Find value with the smallest tentative distance
	shortest_distance.pop(location)
	location = shortest_queue.getMin()[1]
	
	if location == ending:
		print("Shortest Distance to end: ", shortest_distance[ending])
		break

""" Uncomment if you want to see the path """
""" 
print_shortest(shortest_to_create)
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
