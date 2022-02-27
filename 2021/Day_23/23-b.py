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
COMPLETE = [None, None, False, None, False, None, False, None, False, None, None, "A", "A", "A", "A", "B", "B", "B", "B", "C", "C", "C", "C", "D", "D", "D", "D"]

class Position:
	""" Represents any valid position that the amphipods can be in.
	Spots is represented by a list where positions 0-10 are the open row of 
	dots, and spots 11-14 are the side room for A, 15-18 are the side room
	for B, 19-22 are the side room for C, and 23-26 are the side room for D.
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

			if clear:
				sideroom_pos = self.move_into_sideroom(index, "A", positions)
				if sideroom_pos:
					new_pos.append(sideroom_pos)

		# Can skip positions 14, the bottom of its side room
		# Pod is in a side room that it doesn't belong to. Move to either correct
		# side room or into top row.
		elif index != 14:
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

			if clear:
				sideroom_pos = self.move_into_sideroom(index, "B", positions)
				if sideroom_pos:
					new_pos.append(sideroom_pos)

		# Can skip position 18, the bottom of its side room
		# Pod is in a side room that it doesn't belong to. Move to either correct
		# side room or into top row.
		elif index != 18:
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

			if clear:
				sideroom_pos = self.move_into_sideroom(index, "C", positions)
				if sideroom_pos:
					new_pos.append(sideroom_pos)

		# Can skip position 22, the bottom of its side room
		# Pod is in a side room that it doesn't belong to. Move to either correct
		# side room or into top row.
		elif index != 22:
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

			if clear:
				sideroom_pos = self.move_into_sideroom(index, "D", positions)
				if sideroom_pos:
					new_pos.append(sideroom_pos)

		# Can skip position 26, the bottom of its side room
		# Pod is in a side room that it doesn't belong to. Move to either correct
		# side room or into top row.
		elif index != 26:
			new_pos.extend(self.move_from_sideroom("D", positions, 1000, index))

		return new_pos

	def move_into_sideroom(self, index, letter, positions):
		if letter == "A":
			first = 11
			join = 2
			letter_cost = 1
		elif letter == "B":
			first = 15
			join = 4
			letter_cost = 10
		elif letter == "C":
			first = 19
			join = 6
			letter_cost = 100
		elif letter == "D":
			first = 23
			join = 8
			letter_cost = 1000

		pos_copy = copy.copy(positions)

		# Try and move into bottom
		clear = True
		for i in range(first, first + 4):
			if positions[i] != None:
				clear = False
				break
		if clear:
			pos_copy[first + 3] = letter
			pos_copy[index] = None
			cost = (abs(index - join) + 4) * letter_cost

			return Position(pos_copy, cost, self.min_cost + cost)

		# If bottom filled with correct letter, move into 3rd slot
		if positions[first + 3] == letter and\
			positions[first] == None and\
			positions[first + 1] == None and \
			positions[first + 2] == None:

			pos_copy[first + 2] = letter
			pos_copy[index] = None
			cost = (abs(index - join) + 3) * letter_cost

			return Position(pos_copy, cost, self.min_cost + cost)

		# Bottom two are filled with correct letter, add into 2nd spot
		if positions[first + 3] == letter and\
			positions[first + 2] == letter and\
			positions[first] == None and\
			positions[first + 1] == None:

			pos_copy[first + 1] = letter
			pos_copy[index] = None
			cost = (abs(index - join) + 2) * letter_cost

			return Position(pos_copy, cost, self.min_cost + cost)

		# Bottom three are filled with correct letter, add into top spot
		if positions[first + 3] == letter and\
			positions[first + 2] == letter and\
			positions[first + 1] == letter and\
			positions[first] == None:

			pos_copy[first] = letter
			pos_copy[index] = None
			cost = (abs(index - join) + 1) * letter_cost

			return Position(pos_copy, cost, self.min_cost + cost)			

 
		# If top of siderow is blocked, can't move into it
		return False

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
		START_INDEX = [2, 2, 2, 2, 4, 4, 4, 4, 6, 6, 6, 6, 8, 8, 8, 8]
		EXTRA_COST = [1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4]

		start_index_list = []
		extra_cost_list = []
		for i in range(11):
			start_index_list.append(False)
			extra_cost_list.append(False)

		for i in range(len(START_INDEX)):
			start_index_list.append(START_INDEX[i])
			extra_cost_list.append(EXTRA_COST[i])

		start_index = start_index_list[index]
		extra_cost = extra_cost_list[index]

		new_positions = []

		# Letter is blocked in, there are no valid moves for it
		if self.is_blocked_in(index, positions):
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

	def is_blocked_in(self, index, positions):
		# 11-14 are for first side room
		if index <= 14:
			for i in range(index - 1, 11 - 1, -1):
				if positions[i] != None:
					return True

		# 15-18 are for second side room
		elif index <= 18:
			for i in range(index - 1, 15 - 1, -1):
				if positions[i] != None:
					return True

		# 19-22 are for third side room
		elif index <= 22:
			for i in range(index - 1, 19 - 1, -1):
				if positions[i] != None:
					return True

		# 23-26 are for final side room
		else:
			for i in range(index - 1, 23 - 1, -1):
				if positions[i] != None:
					return True

		return False

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
		for i in range(0, 16, 4):
			if self.position[11 + i] != None:
				print(self.position[11 + i], end = "")
			else:
				print(".", end = "")
			print("#", end = "")
		print("##")

		print("###", end = "")
		for i in range(0, 16, 4):
			if self.position[12 + i] != None:
				print(self.position[12 + i], end = "")
			else:
				print(".", end = "")
			print("#", end = "")
		print("##")

		
		print("###", end = "")
		for i in range(0, 16, 4):
			if self.position[13 + i] != None:
				print(self.position[13 + i], end = "")
			else:
				print(".", end = "")
			print("#", end = "")
		print("##")
	
		print("  #", end = "")
		for i in range(0, 16, 4):
			if self.position[14 + i] != None:
				print(self.position[14 + i], end = "")
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

def test_move_from_sideroom():
	positions = ["B", "B", False, None, False, None, False, None, False, "None", "B", "A", "A", "A", "A", None, None, None, "B", "C", "C", "C", "C", "D", "D", "D", "D"]
	test_position = Position(positions, 0, 0)
	new_pos = test_position.move_from_sideroom("B", test_position.position, 10, 18)
	print("Expect 4 options for B to move into. Got", len(new_pos))
	for line in new_pos:
		print(line.position)
		print(line.cost)
		print()

	print(test_position.position)

def test_move_into_sideroom():
	positions = ["D", None, False, None, False, None, False, None, False, "C", "C", None, "A", "A", "A", "B", "B", "B", "B", None, None, None, "C", None, "D", "D", "D"]
	test_position = Position(positions, 0, 0)
	new_pos = test_position.move_into_sideroom(0, "D", test_position.position)

	print(new_pos.position)
	print(new_pos.cost)
	print()
	print(test_position.position)

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

part_2 = ["D", "C", "B", "A", "D", "B", "A", "C"]

for i in range(4):
	initial_pos.append(spots[i])
	initial_pos.append(part_2[i])
	initial_pos.append(part_2[i + 4])
	initial_pos.append(spots[i + 4])

for i in INVALID:
	initial_pos[i] = False

positions = PQueue()
positions.insert_key(Position(initial_pos, 0, 0))

start = timeit.default_timer()

visited = {}
shortest_cost = {}

while len(positions.queue) > 0:
	new_pos = positions.extract_min()
	if new_pos.position == COMPLETE:
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

print("Shortest Path:", shortest_cost.get(tuple(COMPLETE), 999999))

stop = timeit.default_timer()

print('Time: ', stop - start)
