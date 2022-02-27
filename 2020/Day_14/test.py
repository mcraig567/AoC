
def to_binary(number):
    """Takes an integer and converts to a binary list"""
    bin_num = []

    while number > 0:
        bin_num.append(number % 2)
        number = number // 2

    bin_num.reverse()

    return bin_num

def to_dec(number):
    """Takes an array of 0s and 1s (binary number) and converts to base 10"""
    number.reverse()
    out = 0
    for i in range(len(x)):
        out += number[i] * 2 ** i

    return out





x = to_binary(10)
print(x)
print("and back")
x = to_dec(x)
print(x)

