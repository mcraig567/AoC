import timeit
import math
import copy

lines = []
with open("InputTest.txt", "r") as inputFile:
	for line in inputFile:
		line_split = line.split(":")
		position = line_split[1][:-1]
		position.lstrip()
		lines.append(int(position))

### Problem Parameters ###

# Calculate turn % 10. The resulting int is the index in MOVE_DIST.
# MOVE_DIST is the number of spaces forwards that the player travels
MOVE_DIST = [7, 6, 5, 4, 3, 2, 1, 0, 9, 8]

### End Problem Parameters ###

### Helper Functions ###

### End Helper Functions ###

start = timeit.default_timer()

# List where each entry represents a player in the form [position, score]
players = []
for pos in lines:
	players.append([pos, 0])

# Play game
max_score = 0
turn = 0

while max_score < 1000:
	turn += 1

	player_index = (turn % len(players)) - 1
	player = players[player_index]

	movement = MOVE_DIST[turn % 10]
	new_position = player[0] + movement

	if new_position > 10:
		new_position -= 10

	score = player[1] + new_position
	if score > max_score:
		max_score = score

	#print("Player", player_index + 1, "moves to space", new_position, "for a total score of", score)

	player = [new_position, score]

	players[player_index] = player


# Get lowest score
min_score = 99999
for player in players:
	if player[1] < min_score:
		min_score = player[1]

# Determine the answer
times_rolled = turn * 3


print("The die has been rolled", times_rolled, "times")
print("The lowest score was", min_score)
print("Ans:", times_rolled * min_score)

stop = timeit.default_timer()

print('Time: ', stop - start)
