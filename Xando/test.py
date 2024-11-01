import math
import shutil

stars = int(input("How many stars? "))
diameter = 2 * stars + 1

# Get the width of the console
console_width = shutil.get_terminal_size().columns

for i in range(diameter):
    line = ""
    for j in range(diameter):
        if math.sqrt((i - stars) ** 2 + (j - stars) ** 2) <= stars:
            line += "*"
        else:
            line += " "
    # Center the line in the console
    total_leading_spaces = (console_width - len(line)) // 2
    centered_line = " " * total_leading_spaces + line.rstrip()
    print(centered_line)