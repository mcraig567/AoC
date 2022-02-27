
import copy

adapters = []

def read_lines(adapters):
    f = open("C:\\Users\craig\Documents\AoC\Day_10\Input.txt", "r")

    for line in f:
        adapters.append(int(line))

    f.close()

    adapters.sort()

    return adapters

adapters = read_lines(adapters)

option = 1

adapters = adapters + [max(adapters) + 3]

#Number of ways to get to a location is sum of the ways to get to each
#of the 3 numbers before it. Look up in ans, if no adapter for that number
#then 0

#Build ans up as you start from the beginning (dynamic programming)
ans = {}
ans[0] = 1
for a in adapters:
    ans[a] = ans.get(a - 1, 0) + ans.get(a - 2, 0) + ans.get(a - 3, 0)

print(f'Answer: {ans[adapters[-1]]}')