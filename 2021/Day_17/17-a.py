import timeit
import copy

with open("InputTest.txt", "r") as inputFile:
	for line in inputFile:
		inputs = line.split(" ")
		x_limits = inputs[2][2:]
		y_limits = inputs[3][2:]
		x_low, x_high = x_limits.split("..")
		y_low, y_high = y_limits.split("..")

x_low = int(x_low)
x_high = int(x_high[:-1]) # Remove comma
y_low = int(y_low)
y_high = int(y_high)

### Problem Parameters ###

### End Problem Parameters ###

### Helper Functions ###

def is_in_range(val, low, high):
	if val >= low and val <= high:
		return True
	return False

def find_valid_x_turns(low, high):
	turn_dict = {}
	for i in range(high):
		vel = i
		pos = 0
		step = 0

		valid_steps = []
		while pos <= high:
			step += 1
			pos += vel
			
			if vel <= 0:
				if not is_in_range(pos, low, high):
					break
				else:
					valid_steps.append("ONWARDS")
					break
			else:
				vel -= 1

			if is_in_range(pos, low, high):
				valid_steps.append(step)
		
		if len(valid_steps) > 0:
			turn_dict[i] = valid_steps

	return turn_dict

def find_valid_y_turns(low, high):
	""" All upwards velocities hit 0 on turn 2(Vo) at velocity -(Vo + 1)
		Therefore at Vo of abs(y_low) and beyond, guaranteed to miss target zone
	"""
	turn_dict = {}
	max_y = low

	for i in range(low, abs(low)):
		vel = i
		pos = 0
		step = 0

		valid_steps = []
		while pos >= low:
			step += 1
			pos += vel
			vel -= 1

			if is_in_range(pos, low, high):
				#print("initial Vel: ", i,  "is now at position ", pos)
				valid_steps.append(step)

				if i > max_y:
					max_y = i
		
		if len(valid_steps) > 0:
			turn_dict[i] = valid_steps

	return turn_dict, max_y

def get_height(init_vel, max_turn):
	pos = 0
	vel = init_vel
	for i in range(max_turn):
		pos += vel
		vel -= 1
		#print("Height: ", pos)
		if pos == 0:
			print("Initial Vel = ", init_vel, " has hit 0 - turn ", i, " - Velocity: ", vel)
	


### End Helper Functions ###

start = timeit.default_timer()

""" First step - determine what x values will result in hitting the target
	Save into dictionary with number of turns to reach target. If multiple turns,
	create a list
"""
x_turns = find_valid_x_turns(x_low, x_high)
y_turns, max_y = find_valid_y_turns(y_low, y_high)

print(x_turns)

max_height = (max_y * (max_y + 1)) / 2
print("Max Height: ", max_height)

""" Second Step - Determine what steps """




stop = timeit.default_timer()

print('Time: ', stop - start)
