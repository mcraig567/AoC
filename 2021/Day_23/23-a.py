import timeit
import copy

### Problem Parameters ###

COSTS = {
	"A": 1,
	"B": 10,
	"C": 100,
	"D": 1000
}

# Amphipods can't stop in front of a side room
INVALID = [2, 4, 6, 8]

# Finished position
COMPLETE = [None, None, False, None, False, None, False, None, False, None, None, "A", "A", "B", "B", "C", "C", "D", "D"]

class Position:
	""" Represents any valid position that the amphipods can be in.
	Spots is represented by a list where positions 0-10 are the open row of 
	dots, and spots 11-12 are the side room for A, 13-14 are the side room
	for B, 15-16 are the side room for C, and 17-18 are the side room for D.
	If there is no amphipod in a position, it is represented by None,
	otherwise represented by the letter of the amphipod. Spots that cannot be
	filled (invalid positions) are represented by False.
	
	#############
	#...........#
	###A#B#C#D###
  	  #A#B#C#D#
  	  #########

	"""
	def __init__(self, spots, cost, min_cost = 999999):
		self.position = spots
		self.cost = cost
		self.min_cost = min_cost
		self.parent = None

	def __eq__(self, other):
		if other == self.position:
			return True

		return False

	def get_next_pos(self):
		""" Get all valid positions that can be reached from the current position
		
		Returns: An unsorted list of Position objects that can be reached from
		the current position.
		"""
		new_pos = []
		for i in range(len(self.position)):
			positions = []
			char = self.position[i]
			if char == "A":
				positions = self.handle_A_pod(i, self.position)
			elif char == "B":
				positions = self.handle_B_pod(i, self.position)
			elif char == "C":
				positions = self.handle_C_pod(i, self.position)
			elif char == "D":
				positions = self.handle_D_pod(i, self.position)
			
			new_pos.extend(positions)

		return new_pos

	def handle_A_pod(self, index, positions):
		""" Creates a list of Position objects that involve moving an A pod
		
		Requires: index is the starting position of the A pod. Positions is 
		the current position list.

		Returns: An unsorted list of Position objects of all valid places that
		the A pod could move to.		
		"""
		new_pos = []
		first = positions[11]
		second = positions[12]
		join = 2

		# Pod is in the top row, has to go into its side room
		if index < 11:
			# Is the top row clear from index to 2
			clear = True
			if index < join:
				for i in range(index + 1, join):
					if positions[i] != None and positions[i] != False:
						clear = False

			if index > join:
				for i in range (join + 1, index):
					if positions[i] != None and positions[i] != False:
						clear = False

			# Second spot in side room is full, need to move into top spot
			if clear and first == None and second == "A":
				pos_copy = copy.copy(positions)
				pos_copy[11] = "A"
				pos_copy[index] = None
				cost = abs(index - join) + 1

				new_pos.append(Position(pos_copy, cost, self.min_cost + cost))

			# Side room is completely empty, move into second spot
			if clear and first == None and second == None:
				pos_copy = copy.copy(positions)
				pos_copy[12] = "A"
				pos_copy[index] = None
				cost = abs(index - join) + 2

				new_pos.append(Position(pos_copy, cost, self.min_cost + cost))

		# Can skip positions 11 and 12 - If 11 at beginning, would need to move out
		# of side room to let 12 out, or if 12 is A then side room is complete

		# Pod is in a side room that it doesn't belong to. Move to either correct
		# side room or into top row.
		elif index != 12:
			new_pos.extend(self.move_from_sideroom( "A", positions, 1, index))

		return new_pos

	def handle_B_pod(self, index, positions):
		""" Creates a list of Position objects that involve moving an B pod
		
		Requires: index is the starting position of the B pod. Positions is 
		the current position list.

		Returns: An unsorted list of Position objects of all valid places that
		the B pod could move to.		
		"""
		new_pos = []
		first = positions[13]
		second = positions[14]
		join = 4

		# Pod is in the top row, has to go into its side room
		if index < 11:
			# Is the top row clear from index to 4
			clear = True
			if index < join:
				for i in range(index + 1, join):
					if positions[i] != None and positions[i] != False:
						clear = False

			if index > join:
				for i in range (join + 1, index):
					if positions[i] != None and positions[i] != False:
						clear = False

			# Second spot in side room is full, need to move into top spot
			if clear and first == None and second == "B":
				pos_copy = copy.copy(positions)
				pos_copy[13] = "B"
				pos_copy[index] = None
				cost = abs(index - join) * 10 + 10

				new_pos.append(Position(pos_copy, cost, self.min_cost + cost))

			# Side room is completely empty, move into second spot
			if clear and first == None and second == None:
				pos_copy = copy.copy(positions)
				pos_copy[14] = "B"
				pos_copy[index] = None
				cost = abs(index - join) * 10 + 20

				new_pos.append(Position(pos_copy, cost, self.min_cost + cost))

		# Can skip position 14 - If 13 at beginning, would need to move out
		# of side room to let 14 out, or if 14 is B then side room is complete

		# Pod is in a side room that it doesn't belong to. Move to either correct
		# side room or into top row.
		elif index != 14:
			new_pos.extend(self.move_from_sideroom("B", positions, 10, index))

		return new_pos

	def handle_C_pod(self, index, positions):
		""" Creates a list of Position objects that involve moving an C pod
		
		Requires: index is the starting position of the C pod. Positions is 
		the current position list.

		Returns: An unsorted list of Position objects of all valid places that
		the C pod could move to.		
		"""
		new_pos = []
		first = positions[15]
		second = positions[16]
		join = 6

		# Pod is in the top row, has to go into its side room
		if index < 11:
			# Is the top row clear from index to 6
			clear = True
			if index < join:
				for i in range(index + 1, join):
					if positions[i] != None and positions[i] != False:
						clear = False

			if index > join:
				for i in range (join + 1, index):
					if positions[i] != None and positions[i] != False:
						clear = False

			# Second spot in side room is full, need to move into top spot
			if clear and first == None and second == "C":
				pos_copy = copy.copy(positions)
				pos_copy[15] = "C"
				pos_copy[index] = None
				cost = abs(index - join) * 100 + 100

				new_pos.append(Position(pos_copy, cost, self.min_cost + cost))

			# Side room is completely empty, move into second spot
			if clear and first == None and second == None:
				pos_copy = copy.copy(positions)
				pos_copy[16] = "C"
				pos_copy[index] = None
				cost = abs(index - join) * 100 + 200

				new_pos.append(Position(pos_copy, cost, self.min_cost + cost))

		# Can skip position 16 - If 15 at beginning, would need to move out
		# of side room to let 16 out, or if 16 is B then side room is complete

		# Pod is in a side room that it doesn't belong to. Move to either correct
		# side room or into top row.
		elif index != 16:
			new_pos.extend(self.move_from_sideroom("C", positions, 100, index))

		return new_pos

	def handle_D_pod(self, index, positions):
		""" Creates a list of Position objects that involve moving a D pod
		
		Requires: index is the starting position of the D pod. Positions is 
		the current position list.

		Returns: An unsorted list of Position objects of all valid places that
		the D pod could move to.		
		"""
		new_pos = []
		first = positions[17]
		second = positions[18]
		join = 8

		# Pod is in the top row, has to go into its side room
		if index < 11:
			# Is the top row clear from index to 8

			clear = True
			if index < join:
				for i in range(index + 1, join):
					if positions[i] != None and positions[i] != False:
						clear = False

			if index > join:
				for i in range (join + 1, index):
					if positions[i] != None and positions[i] != False:
						clear = False

			# Second spot in side room is full, need to move into top spot
			if clear and first == None and second == "D":
				pos_copy = copy.copy(positions)
				pos_copy[17] = "D"
				pos_copy[index] = None
				cost = abs(index - join) * 1000 + 1000

				new_pos.append(Position(pos_copy, cost, self.min_cost + cost))

			# Side room is completely empty, move into second spot
			if clear and first == None and second == None:
				pos_copy = copy.copy(positions)
				pos_copy[18] = "D"
				pos_copy[index] = None
				cost = abs(index - join) * 1000 + 2000

				new_pos.append(Position(pos_copy, cost, self.min_cost + cost))

		# Can skip position 18 - If 17 at beginning, would need to move out
		# of side room to let 18 out, or if 18 is D then side room is complete

		# Pod is in a side room that it doesn't belong to. Move to either correct
		# side room or into top row.
		elif index != 18:
			new_pos.extend(self.move_from_sideroom("D", positions, 1000, index))

		return new_pos

	def move_from_sideroom(self, letter, positions, cost, index):
		""" Creates a list of Position objects for moving any pod out of any
		sideroom.

		Requires: join index is the index of list at which the side room joins
		the top row. Positions is the current position list. Extra cost is the
		pod's movement cost when moving from the second position in the side 
		room.

		Returns: An unsorted list of valid positions that can be reached by
		moving the specified pod out of the specified side room.		
		"""
		if index == 11:
			start_index = 2
			extra_cost = 1
		elif index == 12:
			start_index = 2
			extra_cost = 2
		elif index == 13:
			start_index = 4
			extra_cost = 1
		elif index == 14:
			start_index = 4
			extra_cost = 2
		elif index == 15:
			start_index = 6
			extra_cost = 1
		elif index == 16:
			start_index = 6
			extra_cost = 2
		elif index == 17:
			start_index = 8
			extra_cost = 1
		else:
			start_index = 8
			extra_cost = 2

		new_positions = []

		# Letter is blocked in, there are no valid moves for it
		if index == 12 or index == 14 or index == 16 or index == 18:
			if positions[index - 1] != None:
				return []

		# Get positions to the left of the side room first
		for i in range(start_index - 1, -1, -1):
			if positions[i] != None and positions[i] != False:
				break

			elif positions[i] != False:
				turn_cost = (start_index - i) * cost + cost * extra_cost
				pos_copy = copy.copy(positions)
				pos_copy[i] = letter
				pos_copy[index] = None
				new_positions.append(Position(pos_copy, turn_cost, self.min_cost + turn_cost))

		# Get positions to the right of the side room
		for i in range(start_index + 1, 11):
			if positions[i] != None and positions[i] != False:
				break
			elif positions[i] != False:
				turn_cost = (i - start_index) * cost + cost * extra_cost
				pos_copy = copy.copy(positions)
				pos_copy[i] = letter
				pos_copy[index] = None
				new_positions.append(Position(pos_copy, turn_cost, self.min_cost + turn_cost))

		return new_positions

	def print_pos(self):
		""" Prints out entire board for debugging """
		for i in range(13):
			print("#", end = "")
		print()

		print("#", end = "")
		for char in self.position[0:11]:
			if char != None and char != False:
				print(char, end = "")
			else:
				print(".", end = "")
		print("#")

		print("###", end = "")
		for i in range(0, 8, 2):
			if self.position[11 + i] != None:
				print(self.position[11 + i], end = "")
			else:
				print(".", end = "")
			print("#", end = "")
		print("##")

		print("  #", end = "")
		for i in range(0, 8, 2):
			if self.position[12 + i] != None:
				print(self.position[12 + i], end = "")
			else:
				print(".", end = "")
			print("#", end = "")
		print("  ")

		print("  #########  ")

class PQueue:
	""" Represents a priority queue where each element is a position in the game. The first
	element in the queue is the position with the least energy required to reach it.
	"""

	def __init__(self, queue = []):
		""" Priority queue is be a binary min-heap with root at index 0 """
		self.queue = queue

	def swap(self, original, new):
		temp = self.queue[original]
		self.queue[original] = self.queue[new]
		self.queue[new] = temp

	def parent(self, i):
		return int((i-1)/2)

	def min_heapify(self, index):
		left = 2 * index + 1
		right = 2 * index + 2
		smallest = index

		if left < len(self.queue) and self.queue[left].min_cost < self.queue[smallest].min_cost:
			smallest = left
		if right < len(self.queue) and self.queue[right].min_cost < self.queue[smallest].min_cost:
			smallest = right

		if smallest != index:
			self.swap(index, smallest)
			self.min_heapify(smallest)

	def insert_key(self, key):
		self.queue.append(key)
		i = len(self.queue) - 1
		
		self.bubble_down(i)

	def bubble_down(self, i):
		moving_val = self.queue[i].min_cost

		while i != 0 and self.queue[self.parent(i)].min_cost > moving_val:
			self.queue[i], self.queue[self.parent(i)] = self.queue[self.parent(i)], self.queue[i]
			i = self.parent(i)

	def extract_min(self):
		root = self.queue[0]
		self.queue[0] = self.queue[-1]
		self.queue.pop()

		if self.queue:
			self.min_heapify(0)

		return root

### End Problem Parameters ###

### Helper Functions ###

### End Helper Functions ###

initial_pos = []
for i in range(11):
	initial_pos.append(None)

with open("Input.txt", "r") as inputFile:
	valid_letters = ["A", "B", "C", "D"]
	spots = []
	for line in inputFile:
		for char in line:
			if char in valid_letters:
				spots.append(char)

for i in range(4):
	initial_pos.append(spots[i])
	initial_pos.append(spots[i+4])

for i in INVALID:
	initial_pos[i] = False

positions = PQueue()
positions.insert_key(Position(initial_pos, 0, 0))

start = timeit.default_timer()

# For each position
# 	- Get all valid positions that can be reached from this position
#	- Add to priority queue
# 	- Pick next position in queue and repeat

visited = {}
shortest_cost = {}
i = 0
while len(positions.queue) > 0:
	i += 1
	""" 	for i in range(len(positions.queue)):
		print(positions.queue[i].min_cost, ", ", end = "")
	print() """

	new_pos = positions.extract_min()
	if new_pos.position == COMPLETE:
		print("Found correct answer")
		break

	if not visited.get(tuple(new_pos.position), False):
		next_positions = new_pos.get_next_pos()
		for turn in next_positions:

			#Turn is currently min cost from new_pos, check against other known paths
			current_cost = shortest_cost.get(tuple(turn.position), 999999)
			if not visited.get(tuple(turn.position), False) and turn.min_cost < current_cost:
				shortest_cost[tuple(turn.position)] = turn.min_cost
				turn.parent = new_pos
				positions.insert_key(turn)

		visited[tuple(new_pos.position)] = True

new_pos.print_pos()
print("Shortest Path:", shortest_cost.get(tuple(COMPLETE), 999999))
print()

""" while new_pos.parent:
	new_pos.print_pos()
	print("Cost:", new_pos.cost)
	new_pos = new_pos.parent
	print() """


stop = timeit.default_timer()

print('Time: ', stop - start)
