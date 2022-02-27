import timeit
import copy

with open("Input.txt", "r") as inputFile:
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

debug_ans = []
with open("Debug.txt", "r") as inputFile:
	for line in inputFile:
		answers = line[:-1].split("   ")
		for sub_ans in answers:
			x, y = sub_ans.split(",")
			debug_ans.append((int(x), int(y)))

### Problem Parameters ###

### End Problem Parameters ###

### Helper Functions ###

def is_in_range(val, low, high):
	if val >= low and val <= high:
		return True
	return False

def find_valid_x_turns(low, high, max_step):
	turn_dict = {}
	for i in range(high + 1):
		vel = i
		pos = 0
		step = 0

		while pos <= high and step <= max_step:
			step += 1
			pos += vel
			
			if vel <= 0:
				if not is_in_range(pos, low, high):
					break
			else:
				vel -= 1

			if is_in_range(pos, low, high):
				x_vels = turn_dict.get(step, [])
				x_vels.append(i)
				turn_dict[step] = x_vels

	return turn_dict

def find_valid_y_turns(low, high):
	""" All upwards velocities hit 0 on turn 2(Vo) at velocity -(Vo + 1)
		Therefore at Vo of abs(y_low) and beyond, guaranteed to miss target zone
	"""
	turn_dict = {}
	max_step = 0

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
				valid_steps.append(step)

				if step > max_step:
					max_step = step
		
		if len(valid_steps) > 0:
			turn_dict[i] = valid_steps

	return turn_dict, max_step

def get_height(init_vel, max_turn):
	pos = 0
	vel = init_vel
	for i in range(max_turn):
		pos += vel
		vel -= 1
		if pos == 0:
			print("Initial Vel = ", init_vel, " has hit 0 - turn ", i, " - Velocity: ", vel)
	
### End Helper Functions ###

start = timeit.default_timer()

""" First step - determine what x values will result in hitting the target
	Save into dictionary with number of turns to reach target. If multiple turns,
	create a list
"""

y_turns, max_step = find_valid_y_turns(y_low, y_high)
x_turns = find_valid_x_turns(x_low, x_high, max_step)

""" Second Step - Determine what steps """
valid_shots = {}
for y_vel in y_turns:
	for turn in y_turns[y_vel]:
		x_vels = x_turns.get(turn, [])
		for x_vel in x_vels:
			valid_shots[(x_vel, y_vel)] = True
			

print(len(valid_shots), "valid shots")

stop = timeit.default_timer()

print('Time: ', stop - start)
