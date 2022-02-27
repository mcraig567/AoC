"""This is actually 4-b as 4-a was saved over"""

#Read input file into list, then close file
initial_dict = {"byr": None, "iyr": None, "eyr": None, "hgt": None, 
        "hcl": None, "ecl": None, "pid": None, "cid": None}
passports = 0
total_pass = 0

f = open("C:\\Users\craig\Documents\AoC\Day_4\Input.txt", "r")

new_dict = dict.fromkeys(initial_dict)

for line in f:
    #print(f"Length of line is {len(line)}")
    if len(line) == 1:
        total_pass = total_pass + 1
        #print("End of Passport")
        
        #CID is optional - overwrite so not None
        new_dict["cid"] = "Overwritten"

        #for key,value in new_dict.items():
        #    print(f"{key} - {value}")

        #If all fields have been added to, passport is ok
        #Reset dictionary with all None values
        if None not in new_dict.values():
            #print()
            #print("This Passport Passes")

            pass_check = False
            BYR_check = False
            IYR_check = False
            EYR_check = False
            HGT_check = False
            HCL_check = False
            ECL_check = False
            PID_check = False

            #Check BYR
            if len(new_dict["byr"]) == 4 and 1920 <= int(new_dict["byr"]) <= 2002:
                BYR_check = True

            #Check IYR
            if len(new_dict["iyr"]) == 4 and 2010 <= int(new_dict["iyr"]) <= 2020:
                IYR_check = True

            #Check EYR
            if len(new_dict["eyr"]) == 4 and 2020 <= int(new_dict["eyr"]) <= 2030:
                EYR_check = True
            
            #Check HGT
            st = new_dict["hgt"][:-2]
            if new_dict["hgt"][-2:] == "cm":
                if 150 <= int(st) <= 193:
                    HGT_check = True

            elif new_dict["hgt"][-2:] == "in":
                if 59 <= int(st) <= 76:
                    HGT_check = True

            #Check HCL
            hcl = new_dict["hcl"]
            if hcl[0] == "#" and len(new_dict["hcl"]) == 7:
                test1 = ["a", "b", "c", "d", "e", "f", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                
                char_test1 = True

                for char in hcl[1:]:
                    if char not in test1:
                        char_test1 = False 
                        break  

                if char_test1:
                    HCL_check = True

            #Check ECL
            ecl = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
            if new_dict["ecl"] in ecl:
                ECL_check = True

            #Check PID
            if len(new_dict["pid"]) == 9:
                test2 = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                char_test = True
                for char in new_dict["pid"]:
                    if char not in test2:
                        char_test = False
                        break

                if char_test:
                    PID_check = True

            if BYR_check and IYR_check and EYR_check and HGT_check and HCL_check and ECL_check and PID_check:
                pass_check = True
            
            
            if pass_check:
                passports = passports + 1
            #print(f"Total passports: {passports}")
            #print()
        
        new_dict = dict.fromkeys(initial_dict)
    
    else:
        pass
        #print(line)

    entries = line.split()

    for entry in entries:
        key = entry.split(":")
        new_dict[key[0]] = key[1]

        

f.close()

print()
print(passports)
print(total_pass)
