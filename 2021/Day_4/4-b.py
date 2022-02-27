import timeit

#Read input file into list, then close file
f = open("Input.txt", "r")

drawnNumbers = []
newBoard = []
boards = []
numberLocations = {} #Key = number, Value = [(board, row, column)]
incompleteBoards = []

boardNumber = -1 #Extra board will be added to boards, want to start actual boards at index 0
row = 0
column = 0

for line in f:
	#Get drawn numbers in order - convert to int
	if len(line) > 20:
		numbers = line.split(",")
		for number in numbers:
			drawnNumbers.append(int(number))

	else:
		boardLine = line.split(" ")
		intBoardLine = []

		if len(boardLine) == 1:
			boards.append(newBoard)
			incompleteBoards.append(boardNumber)
			newBoard = []
			boardNumber += 1
			row = 0
			column = 0

		else:
			for number in boardLine:
				if number != "":
					intNumber = int(number)
					intBoardLine.append(intNumber)

					#Add number to number locations for easy lookup later
					existingNumbers = numberLocations.get(intNumber, [])
					existingNumbers.append((boardNumber, row, column))
					numberLocations[intNumber] = existingNumbers

					column += 1
				
			row += 1
			column = 0


			#print(intBoardLine)
			newBoard.append(intBoardLine)

#Last line doesn't get added automatically, add last board
boards.append(newBoard)
incompleteBoards.append(boardNumber)

#Line between dealt numbers and boards gets added as a board, remove
boards.pop(0)
incompleteBoards.pop(0)

f.close()
 
### HELPER FUNCTIONS ###

#Determines if a board has a BINGO in a row,
#Returns the index of the row if BINGO, otherwise None
def checkRowsForWin(board):
	for row in range(len(board)):
		if sum(board[row]) == -5:
			return row

	return None

#Determines if a board has a BINGO in a column,
#Returns the index of the column if BINGO, otherwise None
def checkColumnsForWin(board):
	for column in range(len(board[0])):
		ans = 0
		for row in board:
			ans += row[column]

		if ans == -5:
			return column

	return None

#Updates all locations given on the provided boards with a -1
def updateBoards(boards, numberLocations):
	for location in numberLocations: #(board, row, column)
		boards[location[0]][location[1]][location[2]] = -1

	return boards

#Returns the index of boards that have won
def checkBoardsForWin(boards, index):
	winningBoards = set() #In case a board wins in both directions at same time
	for i in index:
		rowWin = checkRowsForWin(boards[i])
		if rowWin != None:
			winningBoards.add(i)

		columnWin = checkColumnsForWin(boards[i])
		if columnWin != None:
			winningBoards.add(i)

	return winningBoards

#Returns sum of all unmarked numbers on a board
def sumBoard(board):
	boardTotal = 0
	for row in board:
		for col in row:
			if col != -1:
				boardTotal += col

	return boardTotal

### END HELPER FUNCTIONS ###

start = timeit.default_timer()

totalNumber = 0

#Iterate through the drawn numbers until all boards have won
while incompleteBoards:
	number = drawnNumbers.pop(0)
	totalNumber += 1

	#Update boards with drawn number
	locations = numberLocations[number]
	boards = updateBoards(boards, locations)
	
	#Check any boards that haven't won yet to see if they've now BINGO'd
	completeBoards = checkBoardsForWin(boards, incompleteBoards)
	if len(completeBoards) > 0:		
		for index in completeBoards:
			incompleteBoards.remove(index)

			if len(incompleteBoards) == 0: #Just finished the last board
				winningNumber = number
				winningIndex = index
				break			

ans = sumBoard(boards[winningIndex])
print("ANS:", ans * winningNumber)

stop = timeit.default_timer()

print('Time: ', stop - start)
