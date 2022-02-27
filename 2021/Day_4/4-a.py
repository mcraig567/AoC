
#Read input file into list, then close file
f = open("Input.txt", "r")

drawnNumbers = []
newBoard = []
boards = []
numberLocations = {} #Key = number, Value = [(board, row, column)]

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

#Line between dealt numbers and boards gets added as a board, remove
boards.pop(0)

f.close()
 
### HELPER FUNCTIONS ###
def sumBoardRow(board, row):
	return sum(board[row])

def sumBoardColumn(board, col):
	ans = 0
	for row in board:
		ans += row[col]
	return ans

def checkRowsForWin(board):
	for row in range(len(board)):
		if sum(board[row]) == -5:
			return row

	return None

def checkColumnsForWin(board):
	for column in range(len(board[0])):
		ans = 0
		for row in board:
			ans += row[column]

		if ans == -5:
			return column

	return None

def updateBoards(boards, numberLocations):
	for location in numberLocations: #(board, row, column)
		boards[location[0]][location[1]][location[2]] = -1

	return boards

def checkBoardsForWin(boards):
	for i in range(len(boards)):
		rowWin = checkRowsForWin(boards[i])
		if rowWin != None:
			return (i, rowWin, "row")

		columnWin = checkColumnsForWin(boards[i])
		if columnWin != None:
			return (i, columnWin, "col")

	return None

def sumBoard(board):
	boardTotal = 0
	for row in board:
		for col in row:
			if col != -1:
				boardTotal += col

	return boardTotal


### END HELPER FUNCTIONS ###

totalNumber = 0

for number in drawnNumbers:
	totalNumber += 1
	#print("Number: ", number)

	#Update boards with drawn number
	locations = numberLocations[number]
	boards = updateBoards(boards, locations)
	
	#Check to see if any winning boards
	winningLocation = checkBoardsForWin(boards)
	if winningLocation != None:
		winningNumber = number
		break

print(winningLocation)
print(winningNumber)
print("Total: ", totalNumber)

winningBoard = boards[winningLocation[0]]

ans = sumBoard(winningBoard)
print(ans)

print("TEST ANS:", ans * winningNumber)

""" if winningBoard[2] == "row":
	winningRow = winningLocation[1]
	markedSum = sumBoardRow(winningBoard, winningRow)

else:
	winningColumn = winningLocation[1]
	markedSum = sumBoardColumn(winningBoard, winningColumn)

ans = ans - markedSum
ans = ans * winningNumber
print(ans) """
