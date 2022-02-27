import timeit
import copy

octopusEnergy = {} # Key = (row, column) of octopus, Value = current energy level

f = open("InputTest.txt", "r")
row = 0
for line in f:
	col = 0
	for char in line[:-1]:
		octopusEnergy[(row, col)] = int(char)
		col += 1
	row += 1
f.close()

### Problem Parameters ###


### End Problem Parameters ###

### Helper Functions ###

def hasPopped(octopus):
	if octopus > 9:
		return True
	else:
		return False

def getAffectedOctopi(octopus):
	row = octopus[0]
	column = octopus[1]
	affected = []

	affected.append((row - 1, column - 1)) # Top left corner
	affected.append((row - 1, column)) # Directly above
	affected.append((row - 1, column + 1)) # Top right corner
	affected.append((row, column - 1)) # Directly left
	affected.append((row, column + 1)) # Directly right
	affected.append((row + 1, column - 1)) # Bottom left corner
	affected.append((row + 1, column)) # Directly below
	affected.append((row + 1, column + 1)) # Bottom right corner

	return affected

def increaseAllOctopus(octopusDict):
	for key in octopusDict.keys():
		energy = octopusDict[key]
		energy += 1
		octopusDict[key] = energy

	return octopusDict

def increaseSetOctopus(octopusDict, octopusSet):
	popped = []
	for octopus in octopusSet:
		energy = octopusDict.get(octopus, False)
		if energy:
			energy += 1
			octopusDict[octopus] = energy

			if energy > 9:
				popped.append(octopus)

	return octopusDict, popped

def getSetToPop(octopusDict):
	ans = []
	for key in octopusDict.keys():
		if octopusDict[key] > 9:
			ans.append(key)

	return set(ans)

def printEnergy(octopusDict):
	for i in range(10):
		for j in range(10):
			print("{:<3}".format(octopusDict[(i, j)]), end = "")
		print()

def resetPopped(octopusDict):
	for key in octopusDict.keys():
		if octopusDict[key] > 9:
			octopusDict[key] = 0
	
	return octopusDict


### End Helper Functions ###

start = timeit.default_timer()

totalPopped = 0

for i in range(100):
	octopusEnergy = increaseAllOctopus(octopusEnergy)
	poppedOctopus = list(getSetToPop(octopusEnergy))
	#printEnergy(octopusEnergy)
	#print()

	#print("To Pop: ", poppedOctopus)

	j = 0
	while j < len(poppedOctopus):
		octopus = poppedOctopus[j]
		affectedOctopus = getAffectedOctopi(octopus)
		#print("Affected: ", affectedOctopus)
		octopusEnergy, newPop = increaseSetOctopus(octopusEnergy, affectedOctopus)


		for pop in newPop:
			if pop not in poppedOctopus:
				poppedOctopus.append(pop)
			#poppedOctopus = set(poppedOctopus)
			#poppedOctopus = list(poppedOctopus)

		j += 1

	octopusEnergy = resetPopped(octopusEnergy)
	if len(poppedOctopus) == 100:
		print("ALL POPPED - TURN: ", i)
		break
	
	totalPopped += len(poppedOctopus)

	#printEnergy(octopusEnergy)
	#print()

print("Total Popped: ", totalPopped)

stop = timeit.default_timer()

print('Time: ', stop - start)
