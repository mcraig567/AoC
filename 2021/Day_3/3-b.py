
#Read input file into list, then close file
f = open("Input.txt", "r")

input = []
for line in f:
	input.append(line)
f.close()
 
### HELPER FUNCTIONS ###

def getLargerCountFromList(inputList, index):
	ans = [0, 0, -1]
	for digit in inputList:
		if digit[index] == "0":
			ans[0] += 1
		else:
			ans[1] += 1

	if ans[0] > ans[1]:
		return "0"
	else:
		return "1"

def getSmallerCountFromList(inputList, index):
	tempAns = getLargerCountFromList(inputList, index)
	if tempAns == "0":
		return "1"
	else:
		return "0"

def buildListFromDigitIndex(input, index, digit):
	ans = []
	for number in input:
		if number[index] == digit:
			ans.append(number)

	return ans

### END HELPER FUNCTIONS ###

#Determine the O2 generation and CO2 scrubbing rates
oxygenInput = input.copy()
oxygenIndex = 0
while len(oxygenInput) > 1:
	greaterDigit = getLargerCountFromList(oxygenInput, oxygenIndex)
	oxygenInput = buildListFromDigitIndex(oxygenInput, oxygenIndex, greaterDigit)
	oxygenIndex += 1

CO2Input = input.copy()
CO2Index = 0
while len(CO2Input) > 1:
	smallerDigit = getSmallerCountFromList(CO2Input, CO2Index)
	CO2Input = buildListFromDigitIndex(CO2Input, CO2Index, smallerDigit)
	CO2Index += 1

#Convert binary digits to decimal and return final value
intOxygen = int(oxygenInput[0], 2)
intCO2 = int(CO2Input[0], 2)

print(intOxygen * intCO2)
