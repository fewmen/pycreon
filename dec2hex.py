
def dec2hex(target):
    remainder = []

    while target !=0:
        remainder.append(target % 16)
        target = target // 16

    for i in range(len(remainder)):
        if remainder[i] == 10:
            remainder[i] = 'A'
        elif remainder[i] == 11:
            remainder[i] = 'B'
        elif remainder[i] == 12:
            remainder[i] = 'C'
        elif remainder[i] == 13:
            remainder[i] = 'D'
        elif remainder[i] == 14:
            remainder[i] = 'E'
        elif remainder[i] == 15:
            remainder[i] = 'F'
    remainder.reverse()
    return remainder

print(dec2hex(16))