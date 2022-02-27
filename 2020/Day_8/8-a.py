"""Actually 8-b, saved over 8-a"""

import copy

class game_input:
    def __init__(self, inst, amount):
        self.inst = inst
        self.amount = amount
        self.visited = False
        self.switched = False

    def get_visited(self):
        return self.visited

    def update_visited(self):
        self.visited = True

    def get_inst(self):
        return self.inst

    def set_inst(self, new):
        self.inst = new

    def get_amount(self):
        return self.amount

    def get_switched(self):
        return self.switched
    
    def set_switched(self):
        self.switched = True


#Read input file into list of game_input class, then close file

f = open("C:\\Users\craig\Documents\AoC\Day_8\Input.txt", "r")

lines = []

for line in f:
    #Clean up data - get instruction and amount
    if len(line) > 1:
        split = line.split()
        #print(split)
        #print(split[0])
        #print(int(split[1]))

        x = game_input(split[0], int(split[1]))
        lines.append(x)

f.close()

def print_game(lines):
    for i in range(len(lines)):
        print(f"Location {i} - Direction {lines[i].get_inst()} - Amount {lines[i].get_amount()}")

def game_play(lines, location = 0, score = 0, switch = False):

    # print(f"Location: {location}")
    # print(f"Len(lines): {len(lines)}")
    if location == len(lines):
        print("Location = len(lines)")
        print("Correct Score")
        print(score)
        return score

    play = lines[location]
    # print("New Update")
    # print(f"Direction: {play.get_inst()}")
    # print(f"Amount: {play.get_amount()}")
    # print(f"Seen: {play.get_visited()}")
    # print(f"Score: {score}")
    # print()
    
    while play.get_visited() == False:

        play.update_visited()

        if play.get_inst() == "acc":
            score += play.get_amount()
            return game_play(lines, location + 1, score, switch)

        elif play.get_inst() == "jmp":
            return game_play(lines, location + play.get_amount(), score, switch)

        else:
            return game_play(lines, location + 1, score, switch)   

#print_game(lines)

for i in range(len(lines)):
    #print(f"Checking New Line - {lines[i].get_inst()}")

    #If a line hasn't been switched yet, it should be looked at
    if lines[i].get_switched() == False:
        if lines[i].get_inst() == "nop":
            #print("Switching nop to jmp")
            lines[i].set_inst("jmp")

            #Instructions are seen and marked as seen in the first line. Need to ensure that they do not stay marked when
            #checking the second line
            lines_copy = copy.deepcopy(lines)
            final_score = game_play(lines_copy)
            #print("switching jmp back to nop")
            lines[i].set_inst("nop")

        elif lines[i].get_inst() == "jmp":
            #print("Switching jmp to nop")
            lines[i].set_inst("nop")
            lines_copy = copy.deepcopy(lines)
            final_score = game_play(lines_copy)
            #print("Switching nop back to jmp")
            lines[i].set_inst("jmp")

        #Do not need to run if line is acc - know that it will not work

    lines[i].set_switched()



print(final_score)

