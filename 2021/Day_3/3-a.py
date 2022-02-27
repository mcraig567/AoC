
#Read input file into list, then close file
f = open("Input.txt", "r")

input = []
for line in f:
	input.append(line)
f.close()
 
#Keep number of 0s and 1s in a dictionary
digitCounts = {} #Key = index in digit, Value = [# of 0s, # of 1s, Highest Index]

for binDigit in input:
	for i in range(len(binDigit) - 1):
		count = digitCounts.get(i, [0,0,-1])
		if binDigit[i] == "0":
			count[0] += 1
		else:
			count[1] += 1

		#Keep track of which digit has shown up more
		if count[0] > count[1]:
			count[2] = 0
		else:
			count[2] = 1

		digitCounts[i] = count


#Determine the gamma rate and epsilon rate (in binary) using the values determined above
gammaRate = ""
epsilonRate = ""

for digit in sorted(digitCounts):
	count = digitCounts[digit]

	if count[2] == 0:
		gammaRate = "".join((gammaRate, "0"))
		epsilonRate = "".join((epsilonRate, "1"))
	
	else:
		gammaRate = "".join((gammaRate, "1"))
		epsilonRate = "".join((epsilonRate, "0"))

print(gammaRate)
print(epsilonRate)

intGamma = int(gammaRate, 2)
intEpsilon = int(epsilonRate, 2)

print(intGamma)
print(intEpsilon)

print(intGamma * intEpsilon)


#Returns the index of the larger item in counts - currently only for items length 2
def getGreaterIndex(counts):
	if counts[0] > counts[1]:
		return 0
	else:
		return 1

