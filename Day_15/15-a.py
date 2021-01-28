f = open("C:\\Users\craig\OneDrive\Documents\AoC\Day_15\inputtest.txt", "r")

for line in f:
    initial = line.split(",")
    for i in range(len(initial)):
        initial[i] = int(initial[i])     

f.close()

numbers = {}
turn = 1
number = 0

while turn < 30000000:
    if turn <= len(initial):
        number = initial[turn - 1]

    if number in numbers.keys():
        temp = numbers[number]
        numbers[number] = turn
        number = turn - temp
    else:
        numbers[number] = turn
        number = 0

    turn += 1

print(f"Number {turn} is {number}")