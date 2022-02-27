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

start = timeit.default_timer()

minDistance = 999999999

for meetSpot in range(maxPosition):
	totalDistance = 0
	for spot in crabPositions.keys():
		distance = abs(int(spot) - meetSpot) * crabPositions[spot]
		totalDistance += distance

		minDistance = totalDistance
		minSpot = meetSpot

print("Distance: ", minDistance)
print("Location: ", minSpot)

stop = timeit.default_timer()

print('Time: ', stop - start)
