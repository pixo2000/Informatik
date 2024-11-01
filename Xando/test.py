import math

x = int(input("How many stars? "))

i = 1
while i <= x:
      print(" " * (x - i) + "*" * (2 * i - 1))
            i += 1
      
      i = -x
      while i <= x:
            j = -x
            while j <= x:
                  if math.sqrt(i**2 + j**2) <= x:
                        print("*", end="")
                  else:
                        print(" ", end="")
                  j += 1
            print()
            i += 1