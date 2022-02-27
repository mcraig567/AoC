import timeit
import copy

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

	def get_x_dims(self):
		""" Returns a tuple in the form (min, max) of this Cube in the x direction """
		return (self.x_min, self.x_max)

	def get_y_dims(self):
		""" Returns a tuple in the form (min, max) of this Cube in the y direction """
		return (self.y_min, self.y_max)

	def get_z_dims(self):
		""" Returns a tuple in the form (min, max) of this Cube in the z direction """
		return (self.z_min, self.z_max)

	def get_size(self):
		""" Returns an int representing the size of this Cube """
		return (self.x_max + 1 - self.x_min) * (self.y_max + 1 - self.y_min) * (self.z_max + 1 - self.z_min)

	def get_overlapping(self, other):
		""" Determines if a second Cube has any overlapping reactors with
		this cube. 
		
		Requires: other is a Cube object with any valid dimensions
		
		Returns: a new Cube object with the dimensions of the overlapped
		area shared by this Cube and the other Cube
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

	def split_around_cube(self, other):
		""" Splits the current cube into at most 6 other cubes 
		
			Requires: other is another cube that must overlap the current cube
			at some spot

			Returns: A list of cubes that represent this cube with the overlap
			removed.		
		"""
		
		# Overlap is the entire cube, new cube goes nom
		if other.get_size() == self.get_size():
			return []

		new_cubes = []

		# Get top shelf - y and z are consistent with current cube
		x_max = self.x_max
		x_min = other.get_x_dims()[1] + 1

		if x_max >= x_min:
			top_cube = Cube((x_min, x_max), self.get_y_dims(), self.get_z_dims(), self.type)
			new_cubes.append(top_cube)

		# Get bottom shelf - y and z are consistent with current cube
		x_max = other.get_x_dims()[0] - 1
		x_min = self.x_min

		if x_min <= x_max:
			bottom_cube = Cube((x_min, x_max), self.get_y_dims(), self.get_z_dims(), self.type)
			new_cubes.append(bottom_cube)

		# Get front shelf - x is reduced to top/bottom shelf, z is unchanged
		y_max = other.get_y_dims()[0] - 1
		y_min = self.y_min

		if y_min <= y_max:
			front_cube = Cube(other.get_x_dims(), (y_min, y_max), self.get_z_dims(), self.type)
			new_cubes.append(front_cube)

		# Get back shelf - x is reduced to top/bottom shelf, z in unchanged
		y_max = self.y_max
		y_min = other.get_y_dims()[1] + 1

		if y_max >= y_min:
			back_cube = Cube(other.get_x_dims(), (y_min, y_max), self.get_z_dims(), self.type)
			new_cubes.append(back_cube)

		# Get left shelf - both x and y are reduced to overlap dimensions
		z_max = other.get_z_dims()[0] - 1
		z_min = self.z_min

		if z_min <= z_max:
			left_cube = Cube(other.get_x_dims(), other.get_y_dims(), (z_min, z_max), self.type)
			new_cubes.append(left_cube)	

		# Get right shelf - both x and y are reduced to overlap dimensions
		z_max = self.z_max
		z_min = other.get_z_dims()[1] + 1

		if z_max >= z_min:
			right_cube = Cube(other.get_x_dims(), other.get_y_dims(), (z_min, z_max), self.type)
			new_cubes.append(right_cube)

		return new_cubes	

### End Problem Parameters ###

### Helper Functions ###

def score_cubes(cubes):
	""" Determines the total size of cubes that are 'on' 

		Requires: cubes is a list of cubes

		Returns: an int representing the total size of the cubes	
	"""
	score = 0
	for cube in cubes:
		score += cube.get_size()

	return score

### End Helper Functions ###

lines = []
with open("Input.txt", "r") as inputFile:
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

cubes = []
for i in range(len(lines)):
	cube = lines[i]
	new_cubes = copy.copy(cubes)

	# Compare against all existing cubes, creating a new overlap cube
	for old_cube in cubes:
		overlap = cube.get_overlapping(old_cube)

		# If any overlap, split the old cube.
			# If cube in on-cube, that area will be covered by new cube
			# If cube is off-cube, that area is removed
		if overlap:
			new_cubes.remove(old_cube)
			split_cubes = old_cube.split_around_cube(overlap)
			new_cubes.extend(split_cubes)

	# If cube is on-cube, add to list
	if cube.type == "on":
		new_cubes.append(cube)

	cubes = new_cubes

print("Score:", score_cubes(cubes))

stop = timeit.default_timer()

print('Time: ', stop - start)
