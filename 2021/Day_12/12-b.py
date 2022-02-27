import timeit
import copy

class Cave:
	def __init__(self, name):
		self.name = name
		self.connected_caves = []
		self.times_visited = 0

		# Default to small, but if there's a capital letter, set to large
		self.size = "small"
		for letter in self.name:
			if ord(letter) >= 65 and ord(letter) <= 90:
				self.size = "big"

	def get_size(self):
		return self.size

	def get_name(self):
		return self.name

	def get_connected_caves(self):
		"""Returns a list of cave names that this cave has paths to"""
		return self.connected_caves

	def get_times_visited(self):
		return self.times_visited

	def add_connection(self, cave):
		self.connected_caves.append(cave)

	def add_visit(self):
		self.times_visited += 1

	def remove_visit(self):
		self.times_visited -= 1

class Edge:
	def __init__(self, start, end):
		self.start = start
		self.end = end

	def get_start(self):
		return self.start

	def get_end(self):
		return self.end


caves = {} # Key = name, Value = actual cave object
edges = []
with open("Input.txt", "r") as inputFile:
	for line in inputFile:
		start, end = line.split("-")

		# Remove new line character
		end = end[:-1]

		start_node = caves.get(start, Cave(start))
		end_node = caves.get(end, Cave(end))

		# Add as connected cave
		start_node.add_connection(end_node.get_name())
		end_node.add_connection(start_node.get_name())

		# Save changed node
		caves[start_node.get_name()] = start_node
		caves[end_node.get_name()] = end_node

		# Create new edge
		new_edge = Edge(start_node, end_node)
		if new_edge not in edges:
			edges.append(new_edge)

### Problem Parameters ###

### End Problem Parameters ###

### Helper Functions ###

def check_child_cave(cur_cave, cur_path, cave_dict, paths):
	""" Checks a connected cave to see if there's a path to end cave
		
		Requires current cave name, the path taken to current cave,
		a dictionary of all caves, and the current set of paths to end cave

		Modifies and returns the paths list with any new paths to end cave
	"""
	cave = cave_dict[cur_cave]
	repeated_small_cave = check_path_repeats(cur_path, cave_dict)

	for child in cave.get_connected_caves():
		childCave = cave_dict[child]
		childCave.add_visit()

		if child == "end":
			paths.append(cur_path)

		elif child == "start":
			childCave.remove_visit()

		elif (childCave.get_size() == "small") and (child in cur_path) and repeated_small_cave:
			childCave.remove_visit()
			pass

		else:
			new_path = copy.copy(cur_path)
			new_path.append(child)
			check_child_cave(child, new_path, cave_dict, paths)

	return paths

def remove_val_from_list(old_list, val):
	return [value for value in old_list if value != val]

def get_number_repeats(input_list, val):
	repeats = 0
	for value in input_list:
		if val == value:
			repeats += 1
	return repeats

def check_path_repeats(path, cave_dict):
	""" Checks a list for repeated small caves

		Returns True if a value is repeated more than once,
		returns False otherwise 
	"""
	for cave in path:
		cave_node = cave_dict[cave]
		if cave_node.get_size() == "small":
			repeats = get_number_repeats(path, cave)
			if repeats >= 2:
				return True

	return False

### End Helper Functions ###

start = timeit.default_timer()

# Start with start cave, recursive depth first search to find all valid paths
paths = []
check_child_cave("start", ["start"], caves, paths)

print("LEN: ", len(paths))

stop = timeit.default_timer()

print('Time: ', stop - start)
