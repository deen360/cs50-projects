simport cs50
coin = 0
# gets input from user
x = cs50.get_float("change Owed: ")

# reprompts user for valid input
while x < 0:
    x = cs50.get_float("change Owed: ")
# converts entered input to cents
x = x * 100

# loops through all available input
for i in range(100):
    if x >= 25:
        x = round(x - 25)
        coin += 1
for i in range(100):
    if x >= 10:
        x = round(x - 10)
        coin += 1
for i in range(100):    
    if x >= 5:
        x = round(x - 5)
        coin += 1
for i in range(100):    
    if x >= 1:
        x = round(x - 1)
        coin += 1
    if x == 0:
        break
# prints the coins counted 
print(coin)
    