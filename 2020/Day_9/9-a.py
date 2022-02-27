
f = open("C:\\Users\craig\Documents\AoC\Day_9\Input.txt", "r")

lines = []
all_lines = []
preamble = 25


def read_lines(file, lines, preamble):
    for line in f:
        all_lines.append(int(line))

        #Add preamble to list
        if len(lines) < preamble:
            lines.append(int(line))
            #print(lines)

        #Check to see if next line is valid
        else:
            num = int(line)
            num_check = False

            for i in lines:
                for j in lines:
                    if i + j == num:
                        num_check = True
                        break

            if not num_check:
                #print(f"{num} is not a valid number")
                return num, all_lines[:-1]

            #Remove first number and add newest
            else:
                #print(f"Removing {lines[0]}")
                #print(f"Adding {num}")
                lines.pop(0)
                lines.append(num)
                #print(lines)
                #print()
                

    #If all lines are valid, then return None
    return None


bad_num, all_num = read_lines(f, lines, preamble)
#print(f"BAD {bad_num}")
#print(all_num)

f.close()

def find_sum_nums(nums, total, start):
    num_sum = 0
    end_loc = start
    
    #  0   1   2   3   4   5   6   7   8   9   10   11   12   13
    #[35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182]

    while num_sum <= total:
        # print(f"num_sum: {num_sum}")
        # print(f"start: {start}")
        # print(f"end: {end_loc}")
        # print(f"total: {total}")
        # print()

        #Meet criteria for sum, return the indices of the start and stop location
        if num_sum == total and end_loc - start > 0:
            return start, end_loc

        num_sum += nums[end_loc]
        # print(f"Adding {nums[end_loc]}")
        # print(f"New Sum {num_sum}")
        # print()

        #Move end of sum down the list by one
        end_loc += 1

        #Exit out if gone through list
        if end_loc == len(nums):
            return None, None



    return None, None

for i in range(len(all_num)):
    start, end = find_sum_nums(all_num, bad_num, i)
    if start != None:
        print("OH NO - Start is None")
        break


print(f"start {start}, end {end}")
sum_list = all_num[start : end]
print(sum_list)
minimum = min(sum_list)
maximum = max(sum_list)

print(minimum + maximum)



