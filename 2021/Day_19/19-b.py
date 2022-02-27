import timeit
import math
import copy

### Problem Parameters ###

ROTATIONS = [
	#(1, 2, 3) where 1 = x, 2 = y, 3 = z
	(1, 2, 3),
	(1, -2, -3),
	(1, 3, -2),
	(1, -3, 2),
	(-1, -2, 3),
	(-1, 2, -3),
	(-1, 3, 2),
	(-1, -3, -2),
	(2, 3, 1),
	(2, -3, -1),
	(2, 1, -3),
	(2, -1, 3),
	(-2, 3, -1),
	(-2, -3, 1),
	(-2, 1, 3),
	(-2, -1, -3),
	(3, 1, 2),
	(3, -1, -2),
	(3, 2, -1),
	(3, -2, 1),
	(-3, 1, -2),
	(-3, -1, 2),
	(-3, -2, -1),
	(-3, 2, 1)
]

class Scanner():
	def __init__(self, id):
		self.id = id
		self.beacons = []
		self.rotation = 0
		self.rotated_beacons = []
		self.beacons_relative = []  # Each entry is a dictionary, Key is location realtive to beacon 0, Value is 1 - These will change with rotations		
		self.locked = False
		self.center = None
		self.beacons_to_zero = None
	
	def add_beacon(self, beacon):
		""" Adds a beacon that is seen by the scanner. Beacon coordinates
			should be relative to this scanner.
		"""
		self.beacons.append(beacon)
		self.rotated_beacons.append(beacon)

	def determine_relative_beacons(self):
		""" Create a list where each entry represents a beacon seen by the
			scanner. Each entry is a dictionary showing the distance to every
			other beacon seen by the scanner.
		"""
		self.beacons_relative = []
		for j in range(len(self.rotated_beacons)):
			new_dict = {}
			for i in range(len(self.rotated_beacons)):
				if i == j:
					pass
				else:
					x = self.rotated_beacons[i][0]
					y = self.rotated_beacons[i][1]
					z = self.rotated_beacons[i][2]

					# Determine distance from reference beacon
					rel_x = self.rotated_beacons[j][0] - x
					rel_y = self.rotated_beacons[j][1] - y
					rel_z = self.rotated_beacons[j][2] - z
					rel_pos = (rel_x, rel_y, rel_z)

					new_dict[rel_pos] = 1

			self.beacons_relative.append(new_dict)
				
	def get_beacons(self):
		""" Returns all of the beacons seen by the scanner in its 
			original orientation. 
		"""
		return self.beacons

	def get_relative_beacons(self):
		""" Returns a list where each entry represents a rotated beacon. 
			Each entry is a dictionary with the distance to every other beacon
			seen by the scanner.
		"""
		return self.beacons_relative

	def get_rotated_beacons(self):
		""" Returns all of the beacons as seen by the scanner in its
			current orientation.
		"""
		return self.rotated_beacons

	def get_rotation(self):
		""" Returns an int indicating what rotational position the rotation
			the scanner is currently in.
		"""
		return self.rotation

	def get_lock(self):
		""" Returns true if the correct scanner orientation has been 
			determined,	False otherwise.
		"""
		return self.locked

	def get_abs_locations(self):
		""" Returns all of the beacons seen by the scanner with their 
			positions based off of location (0, 0, 0).
		"""
		return self.beacons_to_zero
	
	def get_center(self):
		""" Returns the location of the scanner based off of position 
			(0, 0, 0).
		"""
		return self.center

	def lock_scanner(self):
		""" Locks scanner to indicate that the correct orientation
			has been determined and no further rotations are necessary.
		"""
		self.locked = True

	def get_shared_positions(self, positions):
		""" Compares the relative beacons of one scanner against
			the relative beacons of this scanner.
		
			Requires: positions is a list of relative beacons where
			each entry is a dictionary representing the distance from
			a beacon to all other beacons seen in that scanner.

			Returns the number of beacons that have identical relative distances
		"""
		for i in range(len(self.beacons_relative)):
			rel_pos_dict = self.beacons_relative[i]
			for j in range(len(positions)):
				beacon = positions[j]
				shared = 0
				pair = None
				for key in beacon:
					shared += rel_pos_dict.get(key, 0)
					pair = (j,i)


				if shared >= 11:
					return shared, pair

		return shared, pair

	def reset_rotation(self):
		""" Sets the scanner back to its original position """
		self.rotation = -1
			
	def apply_rotation(self, ROTATIONS):
		""" Rotates the scanner to the next orientation in the rotation list
		
			Requires: ROTATIONS is the list of all possible orientations the
			scanner can be facing.
		"""
		self.rotated_beacons = []
		self.rotation += 1

		#print("On Rotation:", self.rotation)
		#self.rotation  = self.rotation % 24 # Back to beginning if needed
		current_rotation = ROTATIONS[self.rotation] # = (3, 2, 1)
		
		x = current_rotation[0] # x = 3
		y = current_rotation[1] # y = 2
		z = current_rotation[2] # z = 1

		for beacon in self.beacons:
			new_beacon = [beacon[abs(x) - 1], beacon[abs(y) - 1], beacon[abs(z) - 1]]

			if x < 0:
				new_beacon[0] *= -1

			if y < 0:
				new_beacon[1] *= -1

			if z < 0:
				new_beacon[2] *= -1

			self.rotated_beacons.append(tuple(new_beacon))

	def calculate_center(self, own_beacon, reference_beacon):
		""" Determines and sets the center of the scanner relative to the center
			of a reference scanner. Requires that a beacon can be seen by
			both scanners.

			Requires: own_beacon is the beacon as seen by this scanner.
			reference_beacon is the same beacon seen by another scanner.	
		"""
		center_x = reference_beacon[0] - own_beacon[0]
		center_y = reference_beacon[1] - own_beacon[1]
		center_z = reference_beacon[2] - own_beacon[2]

		self.center = (center_x, center_y, center_z)

	def get_zeroed_locations(self):
		""" Determines the location of each beacon relative to (0, 0, 0) """
		if not self.center:
			return None

		zeroed_beacons = []
		for beacon in self.rotated_beacons:
			x = beacon[0] + self.center[0]
			y = beacon[1] + self.center[1]
			z = beacon[2] + self.center[2]

			zeroed_beacons.append((x, y, z))

		self.beacons_to_zero = zeroed_beacons

### End Problem Parameters ###

### Helper Functions ###

def get_manhattan_distance(beacon1, beacon2):
	""" Determines the manhattan distance between two locations.
	
		Requires: beacon1 is one location in the form (x, y, z). 
		beacon2 is a second location in the same form.

		Returns an int representing the manhattan distance between
		the two  locations	
	"""
	x = abs(beacon1[0] - beacon2[0])
	y = abs(beacon1[1] - beacon2[1])
	z = abs(beacon1[2] - beacon2[2])

	distance = x + y + z
	return distance

### End Helper Functions ###

scanners = []
locked_scanners = []
scanner_id = 1
seen_beacons = 0
with open("Input.txt", "r") as inputFile:
	for line in inputFile:
		if len(line) > 1:
			if line[1] == "-":
				scanner = Scanner(scanner_id)
			else:
				x, y, z = line.split(",")
				x = int(x)
				y = int(y)
				z = int(z[:-1])

				scanner.add_beacon((x, y, z))
				seen_beacons += 1

		else:
			scanner.determine_relative_beacons()
			scanners.append(scanner)
			locked_scanners.append(False)
			scanner_id += 1

# Get last scanner
scanner.determine_relative_beacons()
scanners.append(scanner)
locked_scanners.append(False)

start = timeit.default_timer()

# Use rotation of first scanner as reference for all other scanners
locked_scanners[0] = True
scanners[0].lock_scanner()
scanners[0].center = (0, 0, 0)
scanners[0].rotated_beacons = scanners[0].beacons
scanners[0].beacons_to_zero = scanners[0].beacons

all_beacons = {}
for beacon in scanners[0].get_beacons():
	all_beacons[beacon] = 1

# Iterate through each scanner, keep repeating until all scanners have been locked
while False in locked_scanners:
	for i in range(len(scanners)):
		scanners[i].reset_rotation()
		scanners[i].apply_rotation(ROTATIONS)

		# Look at a scanner in every rotation, then move to the next
		while scanners[i].get_rotation() <= len(ROTATIONS) and locked_scanners[i] == False:
			scanners[i].determine_relative_beacons()
			beacons = scanners[i].get_relative_beacons()

			# Compare scanner against every scanner that is locked, see if any shared beacons
			for j in range(len(locked_scanners)):
				if locked_scanners[j] == True:
					sharedBeacons, pair = scanners[j].get_shared_positions(beacons)

				# Comparing the same beacon and see 11 others = 12 total shared
				if sharedBeacons >= 11: 
					scanners[i].lock_scanner()					
					locked_scanners[i] = True

					scanners[i].calculate_center(scanners[i].get_rotated_beacons()[pair[0]], scanners[j].get_abs_locations()[pair[1]])
					scanners[i].get_zeroed_locations()

					for location in scanners[i].get_abs_locations():
						all_beacons[location] = 1

					break

			if scanners[i].get_lock() or scanners[i].get_rotation() == len(ROTATIONS) - 1:
				break			
			else: 
				scanners[i].apply_rotation(ROTATIONS)


print("There are", len(all_beacons), "beacons in the dict")

# Determine the maximum manhattan distance of all the scanners in the ocean
# Currently O(n^2), however could reduce to O(n) to speed up this part
max_dist = -999999

scanner_centers = []
for scanner in scanners:
	scanner_centers.append(scanner.get_center())

for i in range(len(scanner_centers)):
	for j in range(len(scanner_centers)):
		man_dist = get_manhattan_distance(scanner_centers[i], scanner_centers[j])

		if man_dist > max_dist:
			max_dist = man_dist

print("Max Distance: ", max_dist)

stop = timeit.default_timer()

print('Time: ', stop - start)
