lines = []

f = open("C:\\Users\craig\OneDrive\Documents\AoC\Day_13\input.txt", "r")

for line in f:
    lines.append(line[:-1])
f.close()

time = int(lines[0])
busses = lines[1].split(",")

minimums = []
for i in range(len(busses)):
    minimums.append(0)

print(busses)

all_ok = False

time = 1
step = 1

for i in range(len(busses)):
    if busses[i] != 'x':
        while not all_ok:
            all_ok = True
            left = (time + i) % int(busses[i])

            if left != 0:
                all_ok = False         
                time += step

        all_ok = False
        step = step * int(busses[i])
        

        


print()
print(f"Time: {time}")

# while not all_ok:
#     all_ok = True
#     time += int(busses[0]) #Increase to next multiple of the first bus number
#     #print(time)

#     for i in range(len(busses)):
#         if busses[i] != 'x':
#             # bus_const = int(busses[i])
#             # new_bus = minimums[i]

#             # #Calculate first multiple of next bus number greater than the current time
#             # while new_bus <= time:
#             #     new_bus += bus_const
#             #     minimums[i] = new_bus
#             # #print(new_bus)

#             left = (time + i) % int(busses[i])
#             remainder = int(busses[i]) - left

#             if left != 0:
#                 all_ok = False
#                 break

# print()
# print(f"Time: {time}")
