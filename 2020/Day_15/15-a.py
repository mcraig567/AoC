"""Actually 15-b as 15-a was saved over"""

f = open("C:\\Users\craig\OneDrive\Documents\AoC\Day_15\inputtest.txt", "r")

for line in f:
    initial = line.split(",")
    for i in range(len(initial)):
        initial[i] = int(initial[i])     

f.close()

#Initialize
numbers = {}
turn = 1
number = 0

#play 30000000 turns
while turn < 30000000:
    #Play the first 6 turns
    if turn <= len(initial):
        number = initial[turn - 1]

    #Play the remainder of the turns
    if number in numbers.keys():
        temp = numbers[number]
        numbers[number] = turn
        number = turn - temp
    else:
        numbers[number] = turn
        number = 0

    turn += 1

print(f"Number {turn} is {number}")