#Read input file into list, then close file
f = open("C:\\Users\craig\Documents\AoC\Day_2\Input.txt", "r")

input = []
true = 0

for line in f:
    #Clean up input
    split = line.split(": ")
    reqs = split[0]
    password = split[1]

    split_reqs = reqs.split()
    amounts = split_reqs[0]
    letter = split_reqs[1]

    split_reqs = split_reqs[0].split("-")
    first = int(split_reqs[0])
    second = int(split_reqs[1])

    #print("NEW")
    #print(reqs)
    #print("lower: ", first)
    #print("upper: ", second)
    #print("letter: ", letter)
    #print(password)

    first_char = password[first - 1]
    #print("First: ", first_char)
    second_char = password[second - 1]
    #print("Second: ", second_char)
    #print()

    #Increase true for each passing situation
    if (first_char == letter or second_char == letter) and (first_char != second_char):
        true = true + 1
    #    print("True")

    #print()
      
f.close()

print(true)