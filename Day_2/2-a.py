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
    lower = int(split_reqs[0])
    upper = int(split_reqs[1])

    #print(reqs)
    #print("lower: ", lower)
    #print("upper: ", upper)
    #print("letter: ", letter)
    #print(password)

    letters = {}
    letters[letter] = 0
    for let in password:
        #Can replace with letters.get()
        if let not in letters.keys():
            letters[let] = 1
        else:
            letters[let] = letters[let] + 1

    #print("This many times: ", letters[letter])



    if lower <= letters[letter] <= upper:
        true = true + 1
        #print("True")
    #else:
        #print("False")

    #print()
        
f.close()

print(true)