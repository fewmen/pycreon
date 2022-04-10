
def dec2bin(target):
    remainder = []

    while target != 0:
        remainder.append(target % 2)
        target = target // 2

    remainder.reverse()
    return remainder

print(dec2bin(40))
