import cs50 
# gets user input and prints pyramid 

height = cs50.get_int("Height: ")
while height < 1 or height > 8:
    height = cs50.get_int("Height: ")
for i in range(height):
    #print("-", end="")
    for k in range(height - i - 1):
        print(" ", end="")
    for k in range(i + 1):
        print("#", end="")
    for k in range(1):
        print("  ", end="")
        for k in range(i + 1):
            print("#", end="")
    print()