import timeit

f = open("Input.txt", "r")

crabPositions = {}
maxPosition = 0

for line in f:
	splitLine = line.split(',')
	for num in splitLine:
		currentCrabs = crabPositions.get(num, 0)
		currentCrabs += 1
		crabPositions[num] = currentCrabs

		if int(num) > maxPosition:
			maxPosition = int(num)

f.close()

### HELPER FUNCTIONS ###

def getFuelSpent(start, stop):
	distance = abs(start - stop)
	fuelSpent = distance * (distance + 1) / 2

	return int(fuelSpent)

### END HELPER FUNCTIONS ###

start = timeit.default_timer()

minFuel = 999999999

for meetSpot in range(maxPosition):
	totalFuel = 0
	for spot in crabPositions.keys():
		fuelSpent = getFuelSpent(int(spot), meetSpot)
		spotFuel = fuelSpent * crabPositions[spot]
		totalFuel += spotFuel

	if totalFuel < minFuel:
		minFuel = totalFuel
		minSpot = meetSpot

print("Distance: ", minFuel)
print("Location: ", minSpot)

stop = timeit.default_timer()

print('Time: ', stop - start)
