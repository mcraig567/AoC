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
		self.beacons = []  # Reference beacon will be beacon 0
		self.rotation = 0
		self.rotated_beacons = []
		self.beacons_relative = []  # Each entry is a dictionary, Key is location realtive to beacon 0, Value is 1 - These will change with rotations		
		self.locked = False
		self.center = None
		self.beacons_to_zero = None
	
	def add_beacon(self, beacon):
		self.beacons.append(beacon)
		self.rotated_beacons.append(beacon)

	def determine_relative_beacons(self):
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

					if self.id == 2:
						#print("Check here")
						pass

					# Determine distance from reference beacon
					rel_x = self.rotated_beacons[j][0] - x
					rel_y = self.rotated_beacons[j][1] - y
					rel_z = self.rotated_beacons[j][2] - z
					rel_pos = (rel_x, rel_y, rel_z)

					new_dict[rel_pos] = 1

			self.beacons_relative.append(new_dict)
				
	def get_beacons(self):
		return self.beacons

	def get_relative_beacons(self):
		return self.beacons_relative

	def get_rotated_beacons(self):
		return self.rotated_beacons

	def get_rotation(self):
		return self.rotation

	def get_lock(self):
		return self.locked

	def get_abs_locations(self):
		return self.beacons_to_zero

	def lock_scanner(self):
		self.locked = True

	def is_in_rel_beacon(self, position):
		exists = self.beacons_relative.get(position, None)
		if exists:
			return True

		return False

	def get_shared_positions(self, positions):
		""" Returns the number of beacons that have relative distances"""
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
		self.rotation = -1
			
	def apply_rotation(self, ROTATIONS):
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
		center_x = reference_beacon[0] - own_beacon[0]
		center_y = reference_beacon[1] - own_beacon[1]
		center_z = reference_beacon[2] - own_beacon[2]

		self.center = (center_x, center_y, center_z)

	def get_zeroed_locations(self):
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
scanners[0].rotated_beacons = scanners[0].beacons
scanners[0].beacons_to_zero = scanners[0].beacons

all_beacons = {}
for beacon in scanners[0].get_beacons():
	all_beacons[beacon] = 1

shared = {}

while False in locked_scanners:
	for i in range(len(scanners)):
		scanners[i].reset_rotation()
		scanners[i].apply_rotation(ROTATIONS)
		#print("Reset Rotation:", scanners[i].get_rotation())

		while scanners[i].get_rotation() <= len(ROTATIONS) and locked_scanners[i] == False:
			#print("Examining Scanner ", i, "- Rotation", scanners[i].get_rotation())
			scanners[i].determine_relative_beacons()
			beacons = scanners[i].get_relative_beacons()

			for j in range(len(locked_scanners)):
				if locked_scanners[j] == True:
					#print("Comparing to scanner", j)

					if i == 4 and j == 1 and scanners[i].get_rotation() == 13:
						#print("stop here")
						pass


					sharedBeacons, pair = scanners[j].get_shared_positions(beacons)
					#print("Found", sharedBeacons, "shared beacons")

				# Comparing the same beacon and see 11 others = 12 total shared
				if sharedBeacons >= 11: 
					#print("Found 12 matching beacons - Scanners", j, "and", i)
					#print("Stopped at rotation: ", scanners[i].get_rotation())
					#print("Locking scanner ", i)
					scanners[i].lock_scanner()					
					locked_scanners[i] = True

					#print(pair) # Pair = (m, n) where m is the beacon in scanner[i] that is the same as beacon n in scanner[j]
					#print("In Scanner", i, "beacon ", scanners[i].get_beacons()[pair[0]], " is the same beacon as beacon ", scanners[j].get_beacons()[pair[1]], " of beacon ", j)

					scanners[i].calculate_center(scanners[i].get_rotated_beacons()[pair[0]], scanners[j].get_abs_locations()[pair[1]])
					#print("the center of scanner", i, "is ", scanners[i].center)

					scanners[i].get_zeroed_locations()


					for location in scanners[i].get_abs_locations():
						all_beacons[location] = 1

					shared[(i,j)] = sharedBeacons + 1 # Include reference beacon
					break

			#print("Rotating Scanner ", i + 1, " - New Rotation: ", ROTATIONS[scanners[i].get_rotation() + 1])
			#print()
			if scanners[i].get_lock() or scanners[i].get_rotation() == len(ROTATIONS) - 1:
				break			
			else: 
				scanners[i].apply_rotation(ROTATIONS)
				#print("Now on Rotation:", scanners[i].get_rotation())
			#print()

#print()
print("There are", seen_beacons, "seen beacons, and", sum(shared.values()), "shared beacons")
print("There are", seen_beacons - sum(shared.values()), "total beacons")

print("There are", len(all_beacons), "beacons in the dict")





stop = timeit.default_timer()

print('Time: ', stop - start)
