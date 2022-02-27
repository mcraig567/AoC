import copy

lines = []

f = open("C:\\Users\craig\OneDrive\Documents\AoC\Day_13\input.txt", "r")

pos = 0

for line in f:
    lines.append(line[:-1])
f.close()

time = int(lines[0])
busses = lines[1].split(",")
buss_copy = lines[1].split(",")

# print(busses)
# print(buss_copy)
# print()

for bus in buss_copy:
    if bus == 'x':
        busses.remove('x')

#print(busses)

remainders = [] #Each entry (bus, time to wait)

best_bus = 0
best_time = time
print(time)

for bus in busses:
    print(bus)
    bus_const = int(bus)
    new_bus = int(bus)

    while new_bus <= time:
        new_bus += bus_const
    print(new_bus)

    #remainders.append((bus_const, new_bus % time)

    if new_bus % time < best_time:
        best_bus = bus_const
        best_time = new_bus % time

print(f"Best Bus: {best_bus}")
print(f"Best Time: {best_time}")
print()
print(f"Total: {best_bus * best_time}")

