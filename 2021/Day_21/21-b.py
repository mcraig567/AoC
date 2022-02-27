import timeit
import math
import copy

lines = []
with open("Input.txt", "r") as inputFile:
	for line in inputFile:
		line_split = line.split(":")
		position = line_split[1][:-1]
		position.lstrip()
		lines.append(int(position))

### Problem Parameters ###

# MOVES is a dict of all possible movements that a player will take on
# their turn after rolling three dice. Key = amount moved forwards,
# value = # of universes that are created with this movement in their turn
MOVES = {
	3: 1,
	4: 3,
	5: 6,
	6: 7,
	7: 6,
	8: 3,
	9: 1 
}

### End Problem Parameters ###

### Helper Functions ###

### End Helper Functions ###

start = timeit.default_timer()

# List where each entry represents a player in the form [position, score]
players = []
for pos in lines:
	players.append([pos, 0])

# Universes is a dictionary that keeps track of all universes where the game
# is taking place. Keys are a tuple of tuples (player_1, player_2), where each
# player is of form (position, score). Value is the number of universes with
# that exact scenario
universes = {}
universes[((lines[0], 0), (lines[1], 0))] = 1 # Starting position
wins = [0, 0]

# Play game
max_score = 0
turn = 0

while len(universes) != 0:
	turn += 1
	player_index = (turn % len(players)) - 1
	new_dict = {}

	for entry in universes:
		turn_player = entry[player_index]

		for rolls in MOVES:
			new_position = turn_player[0] + rolls
			if new_position > 10:
				new_position -= 10

			score = turn_player[1] + new_position

			# If a player wins, record the number of universes that they win in
			if score >= 21:
				wins[player_index] += universes[entry] * MOVES[rolls]

			# Otherwise, figure out the new positions that the game can be in
			else:
				key = list(entry)
				key[player_index] = (new_position, score)

				# Possible that we have some overlap with previous entries
				existing_universes = new_dict.get(tuple(key), 0) 
				existing_universes += universes[entry] * MOVES[rolls]
				new_dict[tuple(key)] = existing_universes

	universes = new_dict

print(max(wins))

stop = timeit.default_timer()

print('Time: ', stop - start)
