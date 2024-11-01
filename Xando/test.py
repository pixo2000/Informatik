import math

stars = int(input("How many stars? "))
result = ""
i = 0
while i < (2 * stars) + 1:
        j = 0
        line = ""
        while j < (2 * stars) + 1:
            if math.sqrt((i - stars) ** 2 + (j - stars) ** 2) <= stars:
                line += "*"
            else:
                line += " "
            j += 1
        result += line + "\n"
        i += 1

print(result)