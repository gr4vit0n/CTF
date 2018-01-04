array = [1, 7, 16, 11, 14, 19, 20, 18]
array2 = [85, 111, 117, 43, 104, 127, 117, 117, 33, 110, 99, 43, 72, 95, 85, 85, 94, 66, 120, 98, 79, 117, 68, 83, 64, 94, 39, 65, 73, 32, 65, 72, 51]

flag = ""
num = 0

for factor in array2:
    flag += chr(factor ^ array[num % len(array)])
    num += 1

print(flag)
