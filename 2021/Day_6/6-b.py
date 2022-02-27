import timeit

f = open("Input.txt", "r")

#Array where index is the internal counter of a fish.
#fishCouter[2] gives how many fish have an internal counter of 2
fishCounter = []
for i in range(9):
	fishCounter.append(0)

for line in f:
	splitLine = line.split(',')
	for num in splitLine:
		fishCounter[int(num)] += 1

f.close()

# On each day
# - All fish with a counter of 0 create a new fish with counter 8
# - All fish with a counter of 0 get reset to 6
# - All other counters drop by 1

start = timeit.default_timer()

days = 256
for i in range(days):
	newFish = fishCounter[0]
	for j in range (0, 8):
		fishCounter[j] = fishCounter[j + 1]

	fishCounter[6] += newFish
	fishCounter[8] = newFish

print(sum(fishCounter))

stop = timeit.default_timer()

print('Time: ', stop - start)
