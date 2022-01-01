from cs50 import get_string

words = 0
letters = 0
sentence = 0
# gets text from user
x = get_string("Text:  ")
# converts texts to lower case
x = x.lower()

# iterates through the texts
for text in x:
    if text == (" "):
        words = words + 1
for text in x:
    if text >= "a" and text <= "z":
        letters = letters + 1
for text in x:
    if text == "." or text == "!" or text == "?":
        sentence = sentence + 1
L = (letters / (words + 1)) * 100
S = (sentence / (words + 1)) * 100
index = round(0.0588 * L - 0.296 * S - 15.8)

# prints the grade 
for i in range(16):
    if i == index:
        print(f"Grade {index}")
    
if index < 1:
    print(" Before Grade 1")
    
if index >= 16:
    print("Grade 16+")