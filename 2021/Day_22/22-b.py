import timeit

### Problem Parameters ###

class Cube:
	def __init__(self, x_range, y_range, z_range, type):
		self.x_min = x_range[0]
		self.x_max = x_range[1]
		self.y_min = y_range[0]
		self.y_max = y_range[1]
		self.z_min = z_range[0]
		self.z_max = z_range[1]
		self.type = type
		self.internal_cubes = []

	def get_x_dims(self):
		return (self.x_min, self.x_max)

	def get_y_dims(self):
		return (self.y_min, self.y_max)

	def get_z_dims(self):
		return (self.z_min, self.z_max)

	def is_in(self, node):
		""" Node = (x, y, z)"""
		if node[0] >= self.x_min and node[0] <= self.x_max \
		and node[1] >= self.y_min and node[1] <= self.y_max \
		and node[2] >= self.z_min and node[2] <= self.z_max:
			return True
		
		return False

	def get_size(self):
		return (self.x_max + 1 - self.x_min) * (self.y_max + 1 - self.y_min) * (self.z_max + 1 - self.z_min)

	def get_overlapping(self, other):
		""" Determines if a second Cube has any overlapping reactors with
		this cube. Returns a new Cube with the dimensions of the overlapped
		reators
		"""

		# Get x overlaps		
		other_min = other.get_x_dims()[0]
		other_max = other.get_x_dims()[1]

		if other_min > self.x_max or other_max < self.x_min:
			return None

		if other_min <= self.x_min and other_max >= self.x_max:
			x = (self.x_min, self.x_max)

		elif other_min <= self.x_min and other_max <= self.x_max:
			x = (self.x_min, other_max)

		elif other_min <= self.x_max and other_max >= self.x_max:
			x = (other_min, self.x_max)
		
		else:
			x = other.get_x_dims()

		# Get y overlaps
		other_min = other.get_y_dims()[0]
		other_max = other.get_y_dims()[1]

		if other_min > self.y_max or other_max < self.y_min:
			return None

		if other_min <= self.y_min and other_max >= self.y_max:
			y = [self.y_min, self.y_max]

		elif other_min <= self.y_min and other_max <= self.y_max:
			y = [self.y_min, other_max]

		elif other_min <= self.y_max and other_max >= self.y_max:
			y = [other_min, self.y_max]
		
		else:
			y = other.get_y_dims()

		# Get z overlaps
		other_min = other.get_z_dims()[0]
		other_max = other.get_z_dims()[1]

		if other_min > self.z_max or other_max < self.z_min:
			return None

		if other_min <= self.z_min and other_max >= self.z_max:
			z = [self.z_min, self.z_max]

		elif other_min <= self.z_min and other_max <= self.z_max:
			z = [self.z_min, other_max]

		elif other_min <= self.z_max and other_max >= self.z_max:
			z = [other_min, self.z_max]
		
		else:
			z = other.get_z_dims()		

		return Cube(x, y, z, self.type)

	def add_internal_cube(self, cube):
		self.internal_cubes.append(cube)

	def del_internal_cube(self, cube):
		self.internal_cubes.remove(cube)

	def del_all_internal_cubes(self):
		self.internal_cubes = []

	def create_subsection(self, subcube):
		# Check each sub-cube and trim to size of subsection
		# Check sub-cubes of sub-cube and trim, etc.

		new_cube = Cube(subcube.get_x_dims(), subcube.get_y_dims(), subcube.get_z_dims(), self.type)

		for internal_cube in self.internal_cubes:
			trimmed_cube = self.trim_internal_cube(internal_cube, subcube)
			if trimmed_cube:
				new_cube.add_internal_cube(trimmed_cube)

		return new_cube

	def trim_internal_cube(self, internal_cube, subcube):
		overlap = internal_cube.get_overlapping(subcube)
		
		for sub_cube in internal_cube.internal_cubes:
			trimmed_cube = self.trim_internal_cube(sub_cube, subcube)
			if trimmed_cube:
				overlap.add_internal_cube(trimmed_cube)

		return overlap

### End Problem Parameters ###

### Helper Functions ###

def handle_on_cube(overlap, old_cube):
	overlap = overlap.get_overlapping(old_cube)
	if overlap == None:
		return False
	
	# If on cube fully covers an old on cube, turn all of old cube on
	elif overlap.get_size() == old_cube.get_size() and old_cube.type == "on":
		old_cube.del_all_internal_cubes()

	# Only need to check off cubes to change their state
	elif old_cube.type == "off":
		sub_to_del = []
		for sub_cube in old_cube.internal_cubes:
			sub_overlap = overlap.get_overlapping(sub_cube)

			if sub_overlap != None:
				# If overlap is complete, we can get rid of the sub-cube (all will be on now)
				if sub_overlap.get_size() == sub_cube.get_size():
					sub_to_del.append(sub_cube)

				# Otherwise, some portion of the off sub-cube is turned on, add an on sub-cube
				# within the off sub-cube
				else:
					sub_cube.add_internal_cube(sub_overlap)

		for sub_cube in sub_to_del:
			old_cube.del_internal_cube(sub_cube)

		old_cube.add_internal_cube(overlap)

	# While sub-cubes exist, check all the way down turning on as necessary
	for sub_cube in old_cube.internal_cubes:
		handle_on_cube(overlap, sub_cube)	

	return True

def handle_off_cube(overlap, old_cube):
	overlap = overlap.get_overlapping(old_cube)
	if overlap == None:
		return False

	# If off cube fully covers an old off cube, turn all of old cube off
	if old_cube.type == "off" and overlap.get_size() == old_cube.get_size():
		old_cube.del_all_internal_cubes()	

	# Only need to look at on cubes to change state
	elif old_cube.type == "on":
		sub_to_del = []	
		for sub_cube in old_cube.internal_cubes:
			sub_overlap = overlap.get_overlapping(sub_cube)

			if sub_overlap != None:
				# If overlap is complete, we can get rid of the sub-cube (all will be off now)
				if sub_overlap.get_size() == sub_cube.get_size():
					sub_to_del.append(sub_cube)

				# Otherwise, some portion of the sub-cube is turned off
				else:
					sub_cube.add_internal_cube(sub_overlap)

		for sub_cube in sub_to_del:
			old_cube.del_internal_cube(sub_cube)

		old_cube.add_internal_cube(overlap)

	# While sub-cubes exist, check all the way down turning off as necessary
	for sub_cube in old_cube.internal_cubes:
		handle_off_cube(overlap, sub_cube)

	return True

def score_cube(index, cubes_list):
	cube = cubes_list[index]
	score = cube.get_size()

	# See if cube overlaps with other cubes at all
	for j in range(index + 1, len(cubes_list)):
		next_cube = cubes_list[j]
		if next_cube.type == cube.type:
			
			#Get overlap and remove from score of this cube
			overlap = cube.get_overlapping(next_cube)
			if overlap:
				subsection = cube.create_subsection(overlap)
				subsection_score = score_cube(0, [subsection])
				score -= subsection_score
		
	for i in range(len(cube.internal_cubes)):
		score -= score_cube(i, cube.internal_cubes)

	return score

### End Helper Functions ###

lines = []
with open("InputTest4.txt", "r") as inputFile:
	for line in inputFile:
		all_combinations = []
		switch, params = line.split(" ")
		ranges = params.split(",")
		for dim in ranges:
			dim = dim[2:]
			start, stop = dim.split("..")
			new_list = (int(start), int(stop))
			all_combinations.append(new_list)

		lines.append(Cube(all_combinations[0], all_combinations[1], all_combinations[2], switch))

start = timeit.default_timer()

for i in range(len(lines)):
	#print("new line -", i)
	cube = lines[i]

	# Compare against all existing cubes, creating a new overlap cube
	for j in range(i):
		old_cube = lines[j]
		overlap = cube.get_overlapping(old_cube)
		# If both are on, any off cubes in the overlap are turned on
		if overlap and cube.type == "on" and old_cube.type == "on":
			if overlap.get_size() == old_cube.get_size():
				old_cube.del_all_internal_cubes()
			else:
				handle_on_cube(cube, old_cube)
					
		# If off and comparing to an old on cube, turn overlapping cubes off
		if overlap and cube.type == "off" and old_cube.type == "on":
			handle_off_cube(overlap, old_cube)

### Score cubes ###
score = 0
for i in range(len(lines)):
	if lines[i].type == "on":
		score += score_cube(i, lines)

print("Score:", score)

stop = timeit.default_timer()

print('Time: ', stop - start)
